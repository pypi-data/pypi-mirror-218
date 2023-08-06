import dataclasses
import typing as t

import mantik.unicore.config._base as _base
import mantik.unicore.config._utils as _utils


@dataclasses.dataclass
class Resources(_base.ConfigObject):
    """The computing resources that will be requested ."""

    queue: str
    runtime: t.Optional[str] = None
    nodes: t.Optional[int] = None
    cpus: t.Optional[int] = None
    cpus_per_node: t.Optional[int] = None
    memory: t.Optional[str] = None
    reservation: t.Optional[str] = None
    node_constraints: t.Optional[str] = None
    qos: t.Optional[str] = None

    @classmethod
    def _from_dict(cls, config: t.Dict) -> "Resources":
        queue = _utils.get_required_config_value(
            name="Queue",
            value_type=str,
            config=config,
        )
        runtime = _utils.get_optional_config_value(
            name="Runtime",
            value_type=str,
            config=config,
        )
        nodes = _utils.get_optional_config_value(
            name="Nodes",
            value_type=int,
            config=config,
        )
        cpus = _utils.get_optional_config_value(
            name="CPUs",
            value_type=int,
            config=config,
        )
        cpus_per_node = _utils.get_optional_config_value(
            name="CPUsPerNode",
            value_type=int,
            config=config,
        )
        memory = _utils.get_optional_config_value(
            name="Memory",
            value_type=str,
            config=config,
        )
        reservation = _utils.get_optional_config_value(
            name="Reservation",
            value_type=str,
            config=config,
        )
        node_constraints = _utils.get_optional_config_value(
            name="NodeConstraints",
            value_type=str,
            config=config,
        )
        qos = _utils.get_optional_config_value(
            name="QoS",
            value_type=str,
            config=config,
        )
        return cls(
            queue=queue,
            runtime=runtime,
            nodes=nodes,
            cpus=cpus,
            cpus_per_node=cpus_per_node,
            memory=memory,
            reservation=reservation,
            node_constraints=node_constraints,
            qos=qos,
        )

    def _to_dict(self) -> t.Dict:
        key_values = {
            "Runtime": self.runtime,
            "Queue": self.queue,
            "Nodes": self.nodes,
            "CPUs": self.cpus,
            "CPUsPerNode": self.cpus_per_node,
            "Memory": self.memory,
            "Reservation": self.reservation,
            "NodeConstraints": self.node_constraints,
            "QoS": self.qos,
        }
        return _utils.create_dict_with_not_none_values(**key_values)
