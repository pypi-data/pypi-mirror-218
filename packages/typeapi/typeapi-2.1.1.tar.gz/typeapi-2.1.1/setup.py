# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['typeapi', 'typeapi.backport', 'typeapi.future']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=3.0.0']

setup_kwargs = {
    'name': 'typeapi',
    'version': '2.1.1',
    'description': '',
    'long_description': '# typeapi\n\n[![Python](https://github.com/NiklasRosenstein/python-typeapi/actions/workflows/python.yml/badge.svg)](https://github.com/NiklasRosenstein/python-typeapi/actions/workflows/python.yml)\n\n  [PEP484]: https://peps.python.org/pep-0484/\n  [PEP585]: https://peps.python.org/pep-0585/\n  [PEP604]: https://peps.python.org/pep-0604/\n\n__Compatibility__: Python 3.6.3+\n\nThe `typeapi` package provides an object-oriented interface for introspecting [PEP484][] type hints at runtime,\nincluding forward references that make use of the more recent [PEP585][] and [PEP604][] type hint features in\nPython versions that don\'t natively support them.\n\nThe main API of this module is comprised of:\n\n* `typeapi.TypeHint()` &ndash; A class to parse low-level type hints and present them in a consistent, object-oriented API.\n* `typeapi.get_annotations()` &ndash; Retrieve an object\'s `__annotations__` with support for evaluating future type hints ([PEP585][], [PEP604][]).\n\nThe following kinds of type hints are currently supported:\n\n| Concrete type | Description | Added in |\n| ------------- | ----------- | -------- |\n| `ClassTypeHint` | For any normal or generic type as well as `typing.Any`. Provides access to the underlying type, the type arguments and parameters, if any. | 1.0.0 |\n| `UnionTypeHint` | Represents `Union` type hint and gives access to the union members. | 1.0.0 |\n| `LiteralTypeHint` | Represents a `Literal` type hint and gives access to the literal values. | 1.0.0 |\n| `AnnotatedTypeHint` | Represents an `Annotated` type hint and gives access to the annotated type as well as the metadata. | 1.0.0 |\n| `TypeVarTypeHint` | Represents a `TypeVar` type hint and gives an interface to access the variable\'s metadata (such as constarints, variance, ...). | 1.0.0 |\n| `ForwardRefTypeHint` | Represents a forward reference. Can be evaluated in Python 3.6+ even if it contains [PEP585][] and [PEP604][] expressions. <sup>1)</sup> | 1.0.0, future support in 1.3.0 |\n| `TupleTypeHint` | Reperesents a `Tuple` type hint, allowing you to differentiate between repeated and explicitly sized tuples. | 1.2.0 |\n\n<sup>1)</sup> New-style type union evaluation will continue to return a `typing.Union`, even if the same syntax\nevaluated natively by Python 3.10+ results in a `types.UnionType`.\n\n## Examples\n\nInspect a `List[int]` type hint:\n\n```py\n# cat <<EOF | python -\nfrom typeapi import ClassTypeHint, TypeHint\nfrom typing import List\n\nhint = TypeHint(List[int])\nassert isinstance(hint, ClassTypeHint)\nassert hint.type is list\n\nitem_hint = hint[0]\nassert isinstance(item_hint, ClassTypeHint)\nassert item_hint.type is int\n```\n\nRetrieve the metadata from an `Annotated[...]` type hint:\n\n```py\n# cat <<EOF | python -\nfrom typeapi import AnnotatedTypeHint, ClassTypeHint, TypeHint\nfrom typing_extensions import Annotated\n\nhint = TypeHint(Annotated[int, 42])\nassert isinstance(hint, AnnotatedTypeHint)\nassert hint.type is int\nassert hint.metadata == (42,)\n\nsub_hint = hint[0]\nassert isinstance(sub_hint, ClassTypeHint)\nassert sub_hint.type is int\n```\n\nParameterize one type hint with the parameterization of a generic alias:\n\n```py\n# cat <<EOF | python -\nfrom dataclasses import dataclass\nfrom typeapi import ClassTypeHint, TypeHint\nfrom typing import Generic, TypeVar\nfrom typing_extensions import Annotated\n\nT = TypeVar("T")\n\n@dataclass\nclass MyGeneric(Generic[T]):\n  value: T\n\nhint = TypeHint(MyGeneric[int])\nassert isinstance(hint, ClassTypeHint)\nassert hint.get_parameter_map() == {T: int}\n\nmember_hint = TypeHint(T).parameterize(hint.get_parameter_map())\nassert isinstance(member_hint, ClassTypeHint)\nassert member_hint.type is int\n```\n\nEvaluate forward references with `get_annotations()`:\n\n```py\n# cat <<EOF | python -\nfrom typeapi import get_annotations\nfrom typing import Optional\nfrom sys import version_info\n\nclass MyType:\n  a: "str | None"\n\nannotations = get_annotations(MyType)\n\nif version_info[:2] < (3, 10):\n  assert annotations == {"a": Optional[str]}\nelse:\n  assert annotations == {"a": str | None}\n```\n\nEvaluating forward references with the `TypeHint` API:\n\n```py\n# cat <<EOF | python -\nfrom typeapi import ClassTypeHint, ForwardRefTypeHint, TypeHint\n\nMyVector = "list[MyType]"\n\nclass MyType:\n  pass\n\nhint = TypeHint(MyVector).evaluate(globals())\nprint(hint)  # TypeHint(typing.List[__main__.MyType])\nassert isinstance(hint, ClassTypeHint)\nassert hint.type is list\n\nitem_hint = hint[0]\nassert isinstance(item_hint, ClassTypeHint)\nassert item_hint.type is MyType\n```\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.3,<4.0.0',
}


setup(**setup_kwargs)
