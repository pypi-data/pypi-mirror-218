from __future__ import annotations

import functools
import inspect
from dataclasses import dataclass
from functools import partial
from typing import TYPE_CHECKING, Any, Callable

from pydiverse.pipedag._typing import CallableT
from pydiverse.pipedag.context import ConfigContext, RunContext, TaskContext
from pydiverse.pipedag.core.task import Task
from pydiverse.pipedag.errors import CacheError
from pydiverse.pipedag.materialize.cache import CacheManager, TaskCacheInfo
from pydiverse.pipedag.materialize.container import Blob, Table
from pydiverse.pipedag.util import deep_map
from pydiverse.pipedag.util.hashing import stable_hash

if TYPE_CHECKING:
    from pydiverse.pipedag import Stage


def materialize(
    fn: CallableT = None,
    *,
    name: str = None,
    input_type: type | tuple | dict[str, Any] = None,
    version: str = None,
    cache: Callable = None,
    lazy: bool = False,
    nout: int = 1,
) -> CallableT | MaterializingTask:
    if fn is None:
        return partial(
            materialize,
            name=name,
            input_type=input_type,
            version=version,
            cache=cache,
            lazy=lazy,
            nout=nout,
        )

    return MaterializingTask(
        fn,
        name=name,
        input_type=input_type,
        version=version,
        cache=cache,
        lazy=lazy,
        nout=nout,
    )


class MaterializingTask(Task):
    """Task whose outputs get materialized

    All the values a materializing task returns get written to the appropriate
    storage backend. Additionally, all `Table` and `Blob` objects in the
    input will be replaced with their appropriate objects (loaded from the
    storage backend). This means that tables and blobs never move from one
    task to another directly, but go through the storage layer instead.

    Because of how caching is implemented, task inputs and outputs must all
    be 'materializable'. This means that they can only contain objects of
    the following types:
    `dict`, `list`, `tuple`,
    `int`, `float`, `str`, `bool`, `None`,
    and PipeDAG's `Table` and `Blob` type.

    Automatically adds itself to the active stage.
    All materializing tasks MUST be defined inside a stage.

    :param fn: The run method of this task
    :key name: The name of this task
    :key input_type: The data type to convert table objects to when passed
        to this task.
    :key version: The version of this task. Unless this task is lazy, you
        always have to bump / change the version number to ensure that
        the new implementation gets used. Else a cached result might be used
        instead. version=None and lazy=False means the task is never cached
        but outputs are still materialized.
        In addition, see also option ignore_task_version in pipedag config
        documentation.
    :key cache: An explicit function for validating cache validity. If the output
        of this function changes while the source parameters are the same (e.g.
        the source is a filepath and `cache` loads data from this file), then the
        cache will be deemed invalid and is not used.
    :key lazy: Boolean indicating if this task should be lazy. A lazy task is
        a task that always gets executed, and if it produces a lazy table
        (e.g. a SQL query), the backend can compare the generated output
        to see it the same query has been executed before (and only execute
        it if not). This is an alternative to manually setting the version
        number.
    :key kwargs: Any other keyword arguments will directly get passed to the
        prefect Task initializer.
    """

    def __init__(
        self,
        fn: Callable,
        *,
        name: str = None,
        input_type: type = None,
        version: str = None,
        cache: Callable = None,
        lazy: bool = False,
        nout: int = 1,
    ):
        super().__init__(
            MaterializationWrapper(fn),
            name=name,
            nout=nout,
        )

        self.input_type = input_type
        self.version = version
        self.cache = cache
        self.lazy = lazy

    def run(self, inputs: dict[int, Any], **kwargs):
        # When running only a subset of an entire flow, not all inputs
        # get calculated during flow execution. As a consequence, we must load
        # those inputs from the cache.

        for in_id, in_task in self.input_tasks.items():
            if in_id in inputs:
                continue

            # This returns all metadata objects with the same name, stage, AND position
            # hash as `in_task`. We utilize the position hash to identify a specific
            # task instance, if the same task appears multiple times in a stage.
            store = ConfigContext.get().store
            metadata = store.table_store.retrieve_all_task_metadata(in_task)

            if not metadata:
                raise CacheError(
                    f"Couldn't find cached output for task {in_task}"
                    " with matching position hash."
                )

            output_json = {m.output_json for m in metadata}
            if len(output_json) > 1:
                raise RuntimeError(
                    f"Found multiple matching cached versions of task '{in_task.name}'"
                    f" in stage '{in_task.stage}' with different outputs."
                    f" Couldn't determine which one to use for loading"
                    f" inputs for task {self}."
                )

            # Choose newest entry
            metadata = sorted(metadata, key=lambda m: m.timestamp)[-1]
            cached_output = store.json_decode(metadata.output_json)

            # Load inputs from database
            inputs[in_id] = cached_output

        return super().run(inputs, **kwargs)


@dataclass
class TaskInfo:
    task_cache_info: TaskCacheInfo
    input_tables: list[Table]
    open_stages: set[Stage]


class MaterializationWrapper:
    """Function wrapper that contains all high level materialization logic

    :param fn: The function to wrap
    """

    def __init__(self, fn: Callable):
        functools.update_wrapper(self, fn)

        self.fn = fn
        self.fn_signature = inspect.signature(fn)

    def __call__(self, *args, **kwargs):
        """Function wrapper / materialization logic

        :param args: The arguments passed to the function
        :param _pipedag_task_: The `MaterializingTask` instance which called
            this wrapper.
        :param kwargs: The keyword arguments passed to the function
        :return: A copy of what the original function returns annotated
            with some additional metadata.
        """

        task: MaterializingTask = TaskContext.get().task  # type: ignore
        store = ConfigContext.get().store
        bound = self.fn_signature.bind(*args, **kwargs)

        if task is None:
            raise TypeError("Task can't be None.")

        # If this is the first task in this stage to be executed, ensure that
        # the stage has been initialized and locked.
        store.ensure_stage_is_ready(task.stage)
        open_stages = {task.stage}
        outer_stage = task.stage.outer_stage
        while outer_stage is not None:
            open_stages.add(outer_stage)
            outer_stage = outer_stage.outer_stage

        # Compute the cache key for the task inputs
        input_json = store.json_encode(bound.arguments)
        input_hash = stable_hash("INPUT", input_json)

        cache_fn_hash = ""
        if task.cache is not None:
            cache_fn_output = store.json_encode(task.cache(*args, **kwargs))
            cache_fn_hash = stable_hash("CACHE_FN", cache_fn_output)

        memo_cache_key = CacheManager.task_cache_key(task, input_hash, cache_fn_hash)

        # Check if this task has already been run with the same inputs
        # If yes, return memoized result. This prevents DuplicateNameExceptions
        ctx = RunContext.get()
        with ctx.task_memo(task, memo_cache_key) as (success, memo):
            if success:
                task.logger.info(
                    "Task has already been run with the same inputs."
                    " Using memoized results."
                )

                return memo

            task_cache_info = CacheManager.cache_lookup(
                store, task, input_hash, cache_fn_hash
            )
            if not task.lazy:
                ctx = RunContext.get()
                TaskContext.get().is_cache_valid = task_cache_info.is_cache_valid()
                if task_cache_info.is_cache_valid():
                    ctx.store_task_memo(
                        task, memo_cache_key, task_cache_info.get_cached_output()
                    )
                    # Task isn't lazy -> copy cache to transaction stage
                    return task_cache_info.get_cached_output()
            else:
                # For lazy tasks, is_cache_valid gets set to false during the
                # store.materialize_task procedure
                TaskContext.get().is_cache_valid = True

            # Not found in cache / lazy -> Evaluate Function
            args, kwargs, input_tables = store.dematerialize_task_inputs(
                task, bound.args, bound.kwargs
            )

            result = self.fn(*args, **kwargs)
            result = store.materialize_task(
                task, TaskInfo(task_cache_info, input_tables, open_stages), result
            )

            # Delete underlying objects from result (after materializing them)
            def obj_del_mutator(x):
                if isinstance(x, (Table, Blob)):
                    x.obj = None
                return x

            result = deep_map(result, obj_del_mutator)
            ctx.store_task_memo(task, memo_cache_key, result)
            self.value = result

            return result
