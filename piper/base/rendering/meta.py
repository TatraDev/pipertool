from typing import List, Optional
from dataclasses import dataclass


@dataclass
class FunctionArg:
    name: str
    type_name: str


@dataclass
class Function:
    name: str
    input_args: List[FunctionArg]
    output_args: Optional[List[FunctionArg]] = None


@dataclass
class ExecutorMetaInfo:
    class_name: str
    init_kwargs: dict
    scripts: dict
    async_functions: List[Function]

