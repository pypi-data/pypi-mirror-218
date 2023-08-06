QEMU Machine Protocol client
============================

QMP
---

QEMU Machine Protocol (QMP) is a JSON-based protocol that allows applications to
communicate with a QEMU instance.

For a brief introduction to QMP, see <https://wiki.qemu.org/Documentation/QMP>.

For detailed information about the protocol, see
[QEMU Machine Protocol Specification — QEMU documentation](https://qemu-project.gitlab.io/qemu/interop/qmp-spec.html).

For the full list of commands supported by QMP see
[QEMU QMP Reference Manual — QEMU documentation](https://qemu-project.gitlab.io/qemu/interop/qemu-qmp-ref.html).

About the project
-----------------

This PyPI project packages a single file `qmp.py` from the QEMU source tree:
<https://github.com/qemu/qemu/blob/v5.0.0/python/qemu/qmp.py>.

This PyPI project was created in 2019.

A different project offering a solution to the same problem (and more) has been
created in 2021: <https://pypi.org/project/qemu.qmp/>. You may want to use it.
