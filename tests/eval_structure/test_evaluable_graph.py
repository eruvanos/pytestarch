from typing import List

import pytest
from matplotlib.pyplot import subplots

from pytestarch.eval_structure.evaluable_architecture import (
    EvaluableArchitecture,
    Module,
)
from pytestarch.eval_structure.evaluable_graph import EvaluableArchitectureGraph
from pytestarch.eval_structure.exceptions import ImpossibleMatch
from pytestarch.eval_structure.networkxgraph import NetworkxGraph
from pytestarch.eval_structure_generation.file_import.import_types import AbsoluteImport

MODULE_1 = "Module1"
MODULE_OBJECT_1 = Module(name=MODULE_1)
MODULE_2 = "Module2"
MODULE_OBJECT_2 = Module(name=MODULE_2)
MODULE_3 = "Module3"
MODULE_OBJECT_3 = Module(name=MODULE_3)
MODULE_4 = "Module4"
MODULE_OBJECT_4 = Module(name=MODULE_4)
MODULE_6 = "Module6"
MODULE_OBJECT_6 = Module(name=MODULE_6)
SUB_MODULE_OF_2 = "Module2.SubModule1"
SUB_MODULE_OBJECT_2 = Module(name=SUB_MODULE_OF_2)
SUB_MODULE_OF_1 = "Module1.SubModule1"

MODULE_A = "E.A"  # submodule of E
MODULE_B = "E.A.B"  # submodule of A
MODULE_C = "C"
MODULE_D = "E.A.B.D"  # submodule of B
MODULE_E = "E"
MODULE_F = "E.F"  # submodule of E


@pytest.fixture(scope="module")
def evaluable() -> EvaluableArchitectureGraph:
    all_modules = [MODULE_1, MODULE_2, MODULE_3, MODULE_4, SUB_MODULE_OF_2, MODULE_6]
    imports = [
        AbsoluteImport(MODULE_1, MODULE_2),
        AbsoluteImport(MODULE_1, MODULE_3),
        AbsoluteImport(MODULE_1, MODULE_4),
        AbsoluteImport(MODULE_3, MODULE_2),
        AbsoluteImport(MODULE_4, SUB_MODULE_OF_2),
        AbsoluteImport(MODULE_3, MODULE_6),
    ]

    return EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))


@pytest.fixture(scope="module")
def submodule_evaluable() -> EvaluableArchitectureGraph:
    all_modules = [MODULE_A, MODULE_B, MODULE_C, MODULE_D, MODULE_E, MODULE_F]
    imports = [
        AbsoluteImport(MODULE_F, MODULE_C),
        AbsoluteImport(MODULE_C, MODULE_A),
        AbsoluteImport(MODULE_C, MODULE_B),
    ]

    return EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))


def test_a_depends_on_non_b(evaluable: EvaluableArchitecture) -> None:
    assert evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_1, MODULE_OBJECT_2
    )[MODULE_OBJECT_1]
    assert evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_1, MODULE_OBJECT_3
    )[MODULE_OBJECT_1]
    assert evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_1, MODULE_OBJECT_4
    )[MODULE_OBJECT_1]
    assert evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_1, SUB_MODULE_OBJECT_2
    )[MODULE_OBJECT_1]
    assert evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_1, MODULE_OBJECT_6
    )[MODULE_OBJECT_1]

    assert not evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_2, MODULE_OBJECT_1
    )[MODULE_OBJECT_2]
    assert not evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_2, MODULE_OBJECT_3
    )[MODULE_OBJECT_2]
    assert not evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_2, MODULE_OBJECT_4
    )[MODULE_OBJECT_2]
    assert not evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_2, SUB_MODULE_OBJECT_2
    )[MODULE_OBJECT_2]
    assert not evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_2, MODULE_OBJECT_6
    )[MODULE_OBJECT_2]

    assert evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_3, MODULE_OBJECT_1
    )[MODULE_OBJECT_3]
    assert evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_3, MODULE_OBJECT_2
    )[MODULE_OBJECT_3]
    assert evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_3, MODULE_OBJECT_4
    )[MODULE_OBJECT_3]
    assert evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_3, SUB_MODULE_OBJECT_2
    )[MODULE_OBJECT_3]
    assert evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_3, MODULE_OBJECT_6
    )[MODULE_OBJECT_3]

    assert evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_4, MODULE_OBJECT_1
    )[MODULE_OBJECT_4]
    assert not evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_4, MODULE_OBJECT_2
    )[MODULE_OBJECT_4]
    assert evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_4, MODULE_OBJECT_3
    )[MODULE_OBJECT_4]
    assert not evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_4, SUB_MODULE_OBJECT_2
    )[MODULE_OBJECT_4]
    assert evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_4, MODULE_OBJECT_6
    )[MODULE_OBJECT_4]

    assert not evaluable.any_dependencies_to_modules_other_than(
        SUB_MODULE_OBJECT_2, MODULE_OBJECT_1
    )[SUB_MODULE_OBJECT_2]
    assert not evaluable.any_dependencies_to_modules_other_than(
        SUB_MODULE_OBJECT_2, MODULE_OBJECT_2
    )[SUB_MODULE_OBJECT_2]
    assert not evaluable.any_dependencies_to_modules_other_than(
        SUB_MODULE_OBJECT_2, MODULE_OBJECT_3
    )[SUB_MODULE_OBJECT_2]
    assert not evaluable.any_dependencies_to_modules_other_than(
        SUB_MODULE_OBJECT_2, MODULE_OBJECT_4
    )[SUB_MODULE_OBJECT_2]
    assert not evaluable.any_dependencies_to_modules_other_than(
        SUB_MODULE_OBJECT_2, MODULE_OBJECT_6
    )[SUB_MODULE_OBJECT_2]

    assert not evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_6, MODULE_OBJECT_1
    )[MODULE_OBJECT_6]
    assert not evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_6, MODULE_OBJECT_2
    )[MODULE_OBJECT_6]
    assert not evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_6, MODULE_OBJECT_3
    )[MODULE_OBJECT_6]
    assert not evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_6, MODULE_OBJECT_4
    )[MODULE_OBJECT_6]
    assert not evaluable.any_dependencies_to_modules_other_than(
        MODULE_OBJECT_6, SUB_MODULE_OBJECT_2
    )[MODULE_OBJECT_6]


def test_non_a_depends_on_b(evaluable: EvaluableArchitecture) -> None:
    assert evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_1, MODULE_OBJECT_2
    )[MODULE_OBJECT_2]
    assert not evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_1, MODULE_OBJECT_3
    )[MODULE_OBJECT_3]
    assert not evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_1, MODULE_OBJECT_4
    )[MODULE_OBJECT_4]
    assert evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_1, SUB_MODULE_OBJECT_2
    )[SUB_MODULE_OBJECT_2]
    assert evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_1, MODULE_OBJECT_6
    )[MODULE_OBJECT_6]

    assert not evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_2, MODULE_OBJECT_1
    )[MODULE_OBJECT_1]
    assert evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_2, MODULE_OBJECT_3
    )[MODULE_OBJECT_3]
    assert evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_2, MODULE_OBJECT_4
    )[MODULE_OBJECT_4]
    assert evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_2, SUB_MODULE_OBJECT_2
    )[SUB_MODULE_OBJECT_2]
    assert evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_2, MODULE_OBJECT_6
    )[MODULE_OBJECT_6]

    assert not evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_3, MODULE_OBJECT_1
    )[MODULE_OBJECT_1]
    assert evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_3, MODULE_OBJECT_2
    )[MODULE_OBJECT_2]
    assert evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_3, MODULE_OBJECT_4
    )[MODULE_OBJECT_4]
    assert evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_3, SUB_MODULE_OBJECT_2
    )[SUB_MODULE_OBJECT_2]
    assert not evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_3, MODULE_OBJECT_6
    )[MODULE_OBJECT_6]

    assert not evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_4, MODULE_OBJECT_1
    )[MODULE_OBJECT_1]
    assert evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_4, MODULE_OBJECT_2
    )[MODULE_OBJECT_2]
    assert evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_4, MODULE_OBJECT_3
    )[MODULE_OBJECT_3]
    assert not evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_4, SUB_MODULE_OBJECT_2
    )[SUB_MODULE_OBJECT_2]
    assert evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_4, MODULE_OBJECT_6
    )[MODULE_OBJECT_6]

    assert not evaluable.any_other_dependencies_to_modules_than(
        SUB_MODULE_OBJECT_2, MODULE_OBJECT_1
    )[MODULE_OBJECT_1]
    assert evaluable.any_other_dependencies_to_modules_than(
        SUB_MODULE_OBJECT_2, MODULE_OBJECT_2
    )[MODULE_OBJECT_2]
    assert evaluable.any_other_dependencies_to_modules_than(
        SUB_MODULE_OBJECT_2, MODULE_OBJECT_3
    )[MODULE_OBJECT_3]
    assert evaluable.any_other_dependencies_to_modules_than(
        SUB_MODULE_OBJECT_2, MODULE_OBJECT_4
    )[MODULE_OBJECT_4]
    assert evaluable.any_other_dependencies_to_modules_than(
        SUB_MODULE_OBJECT_2, MODULE_OBJECT_6
    )[MODULE_OBJECT_6]

    assert not evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_6, MODULE_OBJECT_1
    )[MODULE_OBJECT_1]
    assert evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_6, MODULE_OBJECT_2
    )[MODULE_OBJECT_2]
    assert evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_6, MODULE_OBJECT_3
    )[MODULE_OBJECT_3]
    assert evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_6, MODULE_OBJECT_4
    )[MODULE_OBJECT_4]
    assert evaluable.any_other_dependencies_to_modules_than(
        MODULE_OBJECT_6, SUB_MODULE_OBJECT_2
    )[SUB_MODULE_OBJECT_2]


def test_depends_on(evaluable: EvaluableArchitecture) -> None:
    assert evaluable.get_dependencies(MODULE_OBJECT_1, MODULE_OBJECT_2)[
        (MODULE_OBJECT_1, MODULE_OBJECT_2)
    ]
    assert evaluable.get_dependencies(MODULE_OBJECT_1, MODULE_OBJECT_3)[
        (MODULE_OBJECT_1, MODULE_OBJECT_3)
    ]
    assert evaluable.get_dependencies(MODULE_OBJECT_1, MODULE_OBJECT_4)[
        (MODULE_OBJECT_1, MODULE_OBJECT_4)
    ]
    assert not evaluable.get_dependencies(MODULE_OBJECT_1, SUB_MODULE_OBJECT_2)[
        (MODULE_OBJECT_1, SUB_MODULE_OBJECT_2)
    ]
    assert not evaluable.get_dependencies(MODULE_OBJECT_1, MODULE_OBJECT_6)[
        (MODULE_OBJECT_1, MODULE_OBJECT_6)
    ]

    assert not evaluable.get_dependencies(MODULE_OBJECT_2, MODULE_OBJECT_1)[
        (MODULE_OBJECT_2, MODULE_OBJECT_1)
    ]
    assert not evaluable.get_dependencies(MODULE_OBJECT_2, MODULE_OBJECT_3)[
        MODULE_OBJECT_2, MODULE_OBJECT_3
    ]
    assert not evaluable.get_dependencies(MODULE_OBJECT_2, MODULE_OBJECT_4)[
        MODULE_OBJECT_2, MODULE_OBJECT_4
    ]
    assert not evaluable.get_dependencies(
        MODULE_OBJECT_2, Module(name=SUB_MODULE_OF_2)
    )[MODULE_OBJECT_2, SUB_MODULE_OBJECT_2]
    assert not evaluable.get_dependencies(MODULE_OBJECT_2, MODULE_OBJECT_6)[
        (MODULE_OBJECT_2, MODULE_OBJECT_6)
    ]

    assert not evaluable.get_dependencies(MODULE_OBJECT_3, MODULE_OBJECT_1)[
        (MODULE_OBJECT_3, MODULE_OBJECT_1)
    ]
    assert evaluable.get_dependencies(MODULE_OBJECT_3, MODULE_OBJECT_2)[
        (MODULE_OBJECT_3, MODULE_OBJECT_2)
    ]
    assert not evaluable.get_dependencies(MODULE_OBJECT_3, MODULE_OBJECT_4)[
        MODULE_OBJECT_3, MODULE_OBJECT_4
    ]
    assert not evaluable.get_dependencies(MODULE_OBJECT_3, SUB_MODULE_OBJECT_2)[
        (MODULE_OBJECT_3, SUB_MODULE_OBJECT_2)
    ]
    assert evaluable.get_dependencies(MODULE_OBJECT_3, MODULE_OBJECT_6)[
        (MODULE_OBJECT_3, MODULE_OBJECT_6)
    ]

    assert not evaluable.get_dependencies(MODULE_OBJECT_4, MODULE_OBJECT_1)[
        (MODULE_OBJECT_4, MODULE_OBJECT_1)
    ]
    assert evaluable.get_dependencies(MODULE_OBJECT_4, MODULE_OBJECT_2)[
        MODULE_OBJECT_4, MODULE_OBJECT_2
    ]
    assert not evaluable.get_dependencies(MODULE_OBJECT_4, MODULE_OBJECT_3)[
        MODULE_OBJECT_4, MODULE_OBJECT_3
    ]
    assert evaluable.get_dependencies(MODULE_OBJECT_4, SUB_MODULE_OBJECT_2)[
        (MODULE_OBJECT_4, SUB_MODULE_OBJECT_2)
    ]
    assert not evaluable.get_dependencies(MODULE_OBJECT_4, MODULE_OBJECT_6)[
        (MODULE_OBJECT_4, MODULE_OBJECT_6)
    ]

    assert not evaluable.get_dependencies(SUB_MODULE_OBJECT_2, MODULE_OBJECT_1)[
        (SUB_MODULE_OBJECT_2, MODULE_OBJECT_1)
    ]
    assert not evaluable.get_dependencies(SUB_MODULE_OBJECT_2, MODULE_OBJECT_2)[
        (SUB_MODULE_OBJECT_2, MODULE_OBJECT_2)
    ]
    assert not evaluable.get_dependencies(SUB_MODULE_OBJECT_2, MODULE_OBJECT_3)[
        (SUB_MODULE_OBJECT_2, MODULE_OBJECT_3)
    ]
    assert not evaluable.get_dependencies(SUB_MODULE_OBJECT_2, MODULE_OBJECT_4)[
        (SUB_MODULE_OBJECT_2, MODULE_OBJECT_4)
    ]
    assert not evaluable.get_dependencies(SUB_MODULE_OBJECT_2, MODULE_OBJECT_6)[
        (SUB_MODULE_OBJECT_2, MODULE_OBJECT_6)
    ]

    assert not evaluable.get_dependencies(MODULE_OBJECT_6, MODULE_OBJECT_1)[
        (MODULE_OBJECT_6, MODULE_OBJECT_1)
    ]
    assert not evaluable.get_dependencies(MODULE_OBJECT_6, MODULE_OBJECT_2)[
        (MODULE_OBJECT_6, MODULE_OBJECT_2)
    ]
    assert not evaluable.get_dependencies(MODULE_OBJECT_6, MODULE_OBJECT_3)[
        (MODULE_OBJECT_6, MODULE_OBJECT_3)
    ]
    assert not evaluable.get_dependencies(MODULE_OBJECT_6, MODULE_OBJECT_4)[
        (MODULE_OBJECT_6, MODULE_OBJECT_4)
    ]
    assert not evaluable.get_dependencies(MODULE_OBJECT_6, SUB_MODULE_OBJECT_2)[
        (MODULE_OBJECT_6, SUB_MODULE_OBJECT_2)
    ]


def test_submodule_calculation(submodule_evaluable: EvaluableArchitectureGraph) -> None:
    assert submodule_evaluable._get_all_submodules_of(Module(name=MODULE_A)) == {
        MODULE_A,
        MODULE_B,
    }  # D does not show up as it is not connected to any import
    assert submodule_evaluable._get_all_submodules_of(Module(name=MODULE_B)) == {
        MODULE_B
    }  # D does not show up as it is not connected to any import
    assert submodule_evaluable._get_all_submodules_of(Module(name=MODULE_C)) == {
        MODULE_C
    }
    assert submodule_evaluable._get_all_submodules_of(Module(name=MODULE_D)) == {
        MODULE_D
    }
    assert submodule_evaluable._get_all_submodules_of(Module(name=MODULE_E)) == {
        MODULE_E,
        MODULE_A,
        MODULE_B,
        MODULE_F,
    }  # D does not show up as it is not connected to any import
    assert submodule_evaluable._get_all_submodules_of(Module(name=MODULE_F)) == {
        MODULE_F
    }


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(MODULE_1, MODULE_2)],
        [AbsoluteImport(MODULE_1, SUB_MODULE_OF_2)],
        [AbsoluteImport(SUB_MODULE_OF_1, SUB_MODULE_OF_2)],
        [AbsoluteImport(SUB_MODULE_OF_1, MODULE_2)],
    ],
)
def test_is_dependent_between_named_modules(imports: List[AbsoluteImport]) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(name=MODULE_1)
    module_2 = Module(name=MODULE_2)
    assert architecture.get_dependencies(module_1, module_2)[(module_1, module_2)]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(MODULE_1, SUB_MODULE_OF_2)],
        [AbsoluteImport(SUB_MODULE_OF_1, SUB_MODULE_OF_2)],
    ],
)
def test_is_dependent_between_named_and_submodule_modules(
    imports: List[AbsoluteImport],
) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(name=MODULE_1)
    module_2 = Module(parent_module=MODULE_2)
    assert architecture.get_dependencies(module_1, module_2)[(module_1, module_2)]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(SUB_MODULE_OF_1, MODULE_2)],
        [AbsoluteImport(SUB_MODULE_OF_1, SUB_MODULE_OF_2)],
    ],
)
def test_is_dependent_between_submodule_and_named_modules(
    imports: List[AbsoluteImport],
) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(parent_module=MODULE_1)
    module_2 = Module(name=MODULE_2)
    assert architecture.get_dependencies(module_1, module_2)[(module_1, module_2)]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(SUB_MODULE_OF_1, SUB_MODULE_OF_2)],
    ],
)
def test_is_dependent_between_submodule_modules(imports: List[AbsoluteImport]) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(parent_module=MODULE_1)
    module_2 = Module(parent_module=MODULE_2)
    assert architecture.get_dependencies(module_1, module_2)[(module_1, module_2)]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(SUB_MODULE_OF_1, MODULE_1)],
        [AbsoluteImport(SUB_MODULE_OF_2, SUB_MODULE_OF_2)],
    ],
)
def test_is_not_dependent_between_named_modules(imports: List[AbsoluteImport]) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(name=MODULE_1)
    module_2 = Module(name=MODULE_2)
    assert not architecture.get_dependencies(module_1, module_2)[(module_1, module_2)]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(MODULE_1, MODULE_2)],
        [AbsoluteImport(SUB_MODULE_OF_1, MODULE_2)],
    ],
)
def test_is_not_dependent_between_named_and_submodule_modules(
    imports: List[AbsoluteImport],
) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(name=MODULE_1)
    module_2 = Module(parent_module=MODULE_2)
    assert not architecture.get_dependencies(module_1, module_2)[(module_1, module_2)]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(MODULE_1, MODULE_2)],
        [AbsoluteImport(MODULE_1, SUB_MODULE_OF_2)],
    ],
)
def test_is_not_dependent_between_submodule_and_named_modules(
    imports: List[AbsoluteImport],
) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(parent_module=MODULE_1)
    module_2 = Module(name=MODULE_2)
    assert not architecture.get_dependencies(module_1, module_2)[(module_1, module_2)]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(MODULE_1, MODULE_2)],
        [AbsoluteImport(MODULE_1, SUB_MODULE_OF_2)],
        [AbsoluteImport(SUB_MODULE_OF_1, MODULE_2)],
    ],
)
def test_is_not_dependent_between_submodule_modules(
    imports: List[AbsoluteImport],
) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(parent_module=MODULE_1)
    module_2 = Module(parent_module=MODULE_2)
    assert not architecture.get_dependencies(module_1, module_2)[(module_1, module_2)]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(MODULE_1, MODULE_3)],
        [AbsoluteImport(SUB_MODULE_OF_1, MODULE_3)],
    ],
)
def test_any_to_other_between_named_modules(imports: List[AbsoluteImport]) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2, MODULE_3]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(name=MODULE_1)
    module_2 = Module(name=MODULE_2)
    assert architecture.any_dependencies_to_modules_other_than(module_1, module_2)[
        module_1
    ]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(MODULE_1, MODULE_3)],
        [AbsoluteImport(SUB_MODULE_OF_1, MODULE_3)],
        [AbsoluteImport(MODULE_1, MODULE_2)],
        [AbsoluteImport(SUB_MODULE_OF_1, MODULE_2)],
    ],
)
def test_any_to_other_between_named_and_submodule_modules(
    imports: List[AbsoluteImport],
) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2, MODULE_3]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(name=MODULE_1)
    module_2 = Module(parent_module=MODULE_2)
    assert architecture.any_dependencies_to_modules_other_than(module_1, module_2)[
        module_1
    ]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(SUB_MODULE_OF_1, MODULE_3)],
    ],
)
def test_any_to_other_between_submodule_and_named_modules(
    imports: List[AbsoluteImport],
) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2, MODULE_3]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(parent_module=MODULE_1)
    module_2 = Module(name=MODULE_2)
    assert architecture.any_dependencies_to_modules_other_than(module_1, module_2)[
        module_1
    ]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(SUB_MODULE_OF_1, MODULE_3)],
        [AbsoluteImport(SUB_MODULE_OF_1, MODULE_2)],
    ],
)
def test_any_to_other_between_submodule_modules(imports: List[AbsoluteImport]) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2, MODULE_3]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(parent_module=MODULE_1)
    module_2 = Module(parent_module=MODULE_2)
    assert architecture.any_dependencies_to_modules_other_than(module_1, module_2)[
        module_1
    ]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(MODULE_1, MODULE_2)],
        [AbsoluteImport(MODULE_1, SUB_MODULE_OF_2)],
        [AbsoluteImport(SUB_MODULE_OF_1, MODULE_2)],
        [AbsoluteImport(SUB_MODULE_OF_1, SUB_MODULE_OF_2)],
    ],
)
def test_not_any_to_other_between_named_modules(imports: List[AbsoluteImport]) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2, MODULE_3]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(name=MODULE_1)
    module_2 = Module(name=MODULE_2)
    assert not architecture.any_dependencies_to_modules_other_than(module_1, module_2)[
        module_1
    ]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(MODULE_1, SUB_MODULE_OF_2)],
        [AbsoluteImport(SUB_MODULE_OF_1, SUB_MODULE_OF_2)],
    ],
)
def test_not_any_to_other_between_named_and_submodule_modules(
    imports: List[AbsoluteImport],
) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2, MODULE_3]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(name=MODULE_1)
    module_2 = Module(parent_module=MODULE_2)
    assert not architecture.any_dependencies_to_modules_other_than(module_1, module_2)[
        module_1
    ]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(MODULE_1, MODULE_3)],
        [AbsoluteImport(SUB_MODULE_OF_1, MODULE_2)],
        [AbsoluteImport(SUB_MODULE_OF_1, SUB_MODULE_OF_2)],
    ],
)
def test_not_any_to_other_between_submodule_and_named_modules(
    imports: List[AbsoluteImport],
) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2, MODULE_3]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(parent_module=MODULE_1)
    module_2 = Module(name=MODULE_2)
    assert not architecture.any_dependencies_to_modules_other_than(module_1, module_2)[
        module_1
    ]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(MODULE_1, MODULE_3)],
        [AbsoluteImport(SUB_MODULE_OF_1, SUB_MODULE_OF_2)],
    ],
)
def test_not_any_to_other_between_submodule_modules(
    imports: List[AbsoluteImport],
) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2, MODULE_3]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(parent_module=MODULE_1)
    module_2 = Module(parent_module=MODULE_2)
    assert not architecture.any_dependencies_to_modules_other_than(module_1, module_2)[
        module_1
    ]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(MODULE_3, MODULE_2)],
        [AbsoluteImport(MODULE_3, SUB_MODULE_OF_2)],
    ],
)
def test_other_to_module_than_between_named_modules(
    imports: List[AbsoluteImport],
) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2, MODULE_3]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(name=MODULE_1)
    module_2 = Module(name=MODULE_2)
    assert architecture.any_other_dependencies_to_modules_than(module_1, module_2)[
        module_2
    ]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(MODULE_3, SUB_MODULE_OF_2)],
    ],
)
def test_other_to_module_than_between_named_and_submodule_modules(
    imports: List[AbsoluteImport],
) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2, MODULE_3]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(name=MODULE_1)
    module_2 = Module(parent_module=MODULE_2)
    assert architecture.any_other_dependencies_to_modules_than(module_1, module_2)[
        module_2
    ]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(MODULE_1, MODULE_2)],
        [AbsoluteImport(MODULE_1, SUB_MODULE_OF_2)],
        [AbsoluteImport(MODULE_3, MODULE_2)],
        [AbsoluteImport(MODULE_3, SUB_MODULE_OF_2)],
    ],
)
def test_other_to_module_than_between_submodule_and_named_modules(
    imports: List[AbsoluteImport],
) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2, MODULE_3]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(parent_module=MODULE_1)
    module_2 = Module(name=MODULE_2)
    assert architecture.any_other_dependencies_to_modules_than(module_1, module_2)[
        module_2
    ]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(MODULE_1, SUB_MODULE_OF_2)],
        [AbsoluteImport(MODULE_3, SUB_MODULE_OF_2)],
    ],
)
def test_other_to_module_than_between_submodule_modules(
    imports: List[AbsoluteImport],
) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2, MODULE_3]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(parent_module=MODULE_1)
    module_2 = Module(parent_module=MODULE_2)
    assert architecture.any_other_dependencies_to_modules_than(module_1, module_2)[
        module_2
    ]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(MODULE_1, MODULE_2)],
        [AbsoluteImport(MODULE_1, SUB_MODULE_OF_2)],
        [AbsoluteImport(SUB_MODULE_OF_1, MODULE_2)],
        [AbsoluteImport(SUB_MODULE_OF_1, SUB_MODULE_OF_2)],
    ],
)
def test_not_other_to_module_than_between_named_modules(
    imports: List[AbsoluteImport],
) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2, MODULE_3]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(name=MODULE_1)
    module_2 = Module(name=MODULE_2)
    assert not architecture.any_other_dependencies_to_modules_than(module_1, module_2)[
        module_2
    ]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(MODULE_1, SUB_MODULE_OF_2)],
        [AbsoluteImport(SUB_MODULE_OF_1, SUB_MODULE_OF_2)],
        [AbsoluteImport(MODULE_3, MODULE_2)],
    ],
)
def test_not_other_to_module_than_between_named_and_submodule_modules(
    imports: List[AbsoluteImport],
) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2, MODULE_3]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(name=MODULE_1)
    module_2 = Module(parent_module=MODULE_2)
    assert not architecture.any_other_dependencies_to_modules_than(module_1, module_2)[
        module_2
    ]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(SUB_MODULE_OF_1, MODULE_2)],
        [AbsoluteImport(SUB_MODULE_OF_1, SUB_MODULE_OF_2)],
    ],
)
def test_not_other_to_module_than_between_submodule_and_named_modules(
    imports: List[AbsoluteImport],
) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2, MODULE_3]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(parent_module=MODULE_1)
    module_2 = Module(name=MODULE_2)
    assert not architecture.any_other_dependencies_to_modules_than(module_1, module_2)[
        module_2
    ]


@pytest.mark.parametrize(
    "imports",
    [
        [AbsoluteImport(MODULE_1, MODULE_2)],
        [AbsoluteImport(SUB_MODULE_OF_1, MODULE_2)],
        [AbsoluteImport(SUB_MODULE_OF_1, SUB_MODULE_OF_2)],
        [AbsoluteImport(MODULE_3, MODULE_2)],
    ],
)
def test_not_other_to_module_than_between_submodule_modules(
    imports: List[AbsoluteImport],
) -> None:
    all_modules = [MODULE_1, MODULE_2, SUB_MODULE_OF_1, SUB_MODULE_OF_2, MODULE_3]
    architecture = EvaluableArchitectureGraph(NetworkxGraph(all_modules, imports))

    module_1 = Module(parent_module=MODULE_1)
    module_2 = Module(parent_module=MODULE_2)
    assert not architecture.any_other_dependencies_to_modules_than(module_1, module_2)[
        module_2
    ]


def test_all_modules_labeled_when_aliases_used(
    evaluable: EvaluableArchitecture,
) -> None:
    module_1_alias = "1"
    aliases = {MODULE_1: module_1_alias}
    fig, ax = subplots()

    evaluable.visualize(aliases=aliases, ax=ax)

    labels_in_plot = [t.get_text() for t in ax.texts]
    assert len(labels_in_plot) == 6


def test_alias_replaces_module_name_in_plot(evaluable: EvaluableArchitecture) -> None:
    module_2_alias = "2"
    aliases = {MODULE_2: module_2_alias}
    fig, ax = subplots()

    evaluable.visualize(aliases=aliases, ax=ax)

    labels_in_plot = [t.get_text() for t in ax.texts]
    assert module_2_alias in labels_in_plot
    assert MODULE_2 not in labels_in_plot
    assert SUB_MODULE_OF_2 not in labels_in_plot
    assert f"{module_2_alias}.SubModule1" in labels_in_plot


def test_alias_replaces_module_name_in_submodules_plot(
    evaluable: EvaluableArchitecture,
) -> None:
    module_2_alias = "2"
    aliases = {MODULE_2: module_2_alias}
    submodule_label_with_alias = f"{module_2_alias}.SubModule1"
    fig, ax = subplots()

    evaluable.visualize(aliases=aliases, ax=ax)

    labels_in_plot = [t.get_text() for t in ax.texts]
    assert module_2_alias in labels_in_plot
    assert MODULE_2 not in labels_in_plot
    assert SUB_MODULE_OF_2 not in labels_in_plot
    assert submodule_label_with_alias in labels_in_plot


def test_when_module_and_a_submodule_have_aliases_the_submodule_alias_takes_priority(
    submodule_evaluable: EvaluableArchitecture,
) -> None:
    module_e_alias = "e"
    submodule_of_e_alias = "ea"
    submodule_label_with_parent_alias = f"{module_e_alias}.A"
    aliases = {MODULE_E: module_e_alias, MODULE_A: submodule_of_e_alias}
    fig, ax = subplots()

    submodule_evaluable.visualize(aliases=aliases, ax=ax)

    labels_in_plot = [t.get_text() for t in ax.texts]
    assert module_e_alias in labels_in_plot
    assert submodule_of_e_alias in labels_in_plot
    assert SUB_MODULE_OF_2 not in labels_in_plot
    assert submodule_label_with_parent_alias not in labels_in_plot
    assert f"{module_e_alias}.F" in labels_in_plot


def test_when_module_name_in_alias_spec_is_not_found_an_error_is_raised(
    evaluable: EvaluableArchitecture,
) -> None:
    non_existent_module = "non_existent_module"
    aliases = {non_existent_module: "a"}

    with pytest.raises(KeyError, match=non_existent_module):
        evaluable.visualize(aliases=aliases)


MODULE = "test.module.submodule.class"


partial_match_test_cases = [
    pytest.param("test.module.submodule.class", True, id="complete match - match"),
    pytest.param("test.module.submodule.clasz", False, id="complete match - no match"),
    pytest.param("*.class", True, id="end match - match"),
    pytest.param("*.clasz", False, id="end match - no match"),
    pytest.param("test.*", True, id="start match - match"),
    pytest.param("test,*", False, id="start match - no match"),
    pytest.param("*le.submo*", True, id="inner match - match"),
    pytest.param("les.submo*", False, id="inner match - no match"),
]


@pytest.mark.parametrize("match, expected_result", partial_match_test_cases)
def test_partial_match(match: str, expected_result: bool) -> None:
    assert (
        EvaluableArchitectureGraph._partial_name_match(match, MODULE) == expected_result
    )


def test_module_matches(submodule_evaluable: EvaluableArchitectureGraph) -> None:
    module_matches = [
        Module(name="*D", partial_match=True),
        Module(name="*A*", partial_match=True),
    ]

    calculated_matches = submodule_evaluable._convert_to_full_name_matches(
        [module_matches]
    )

    assert len(calculated_matches) == 1
    assert len(calculated_matches[0]) == 3

    assert Module(name=MODULE_A) in calculated_matches[0]
    assert Module(name=MODULE_B) in calculated_matches[0]
    assert Module(name=MODULE_D) in calculated_matches[0]


def test_non_partial_module_does_not_match_anything_but_itself(
    submodule_evaluable: EvaluableArchitectureGraph,
) -> None:
    module_matches = [Module(name="*.*")]

    calculated_matches = submodule_evaluable._convert_to_full_name_matches(
        [module_matches]
    )

    assert len(calculated_matches) == 1
    assert len(calculated_matches[0]) == 1

    assert Module(name="*.*") in calculated_matches[0]


def test_never_matched_match_raises_error(
    evaluable: EvaluableArchitectureGraph,
) -> None:
    module_matches = [Module(name="I will not match", partial_match=True)]

    with pytest.raises(
        ImpossibleMatch, match="No modules found that match: I will not match"
    ):
        evaluable._convert_to_full_name_matches([module_matches])


def test_module_matches_reported_separately_by_group(
    submodule_evaluable: EvaluableArchitectureGraph,
) -> None:
    module_matches_1 = [
        Module(name="*D", partial_match=True),
    ]

    module_matches_2 = [
        Module(name="*A*", partial_match=True),
    ]

    calculated_matches = submodule_evaluable._convert_to_full_name_matches(
        [module_matches_1, module_matches_2]
    )

    assert len(calculated_matches) == 2

    assert len(calculated_matches[0]) == 1
    assert len(calculated_matches[1]) == 3

    assert Module(name=MODULE_D) in calculated_matches[0]
    assert Module(name=MODULE_A) in calculated_matches[1]
    assert Module(name=MODULE_B) in calculated_matches[1]
    assert Module(name=MODULE_D) in calculated_matches[1]
