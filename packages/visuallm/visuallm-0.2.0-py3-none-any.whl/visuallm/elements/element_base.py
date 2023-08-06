from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, Optional

from visuallm.component_base import ComponentBase
from visuallm.named import Named, NamedWrapper

from .utils import register_named, sanitize_url

if TYPE_CHECKING:
    from visuallm.server import Server


class ElementBase(Named, ABC):
    """Base class for all elements in a single component. Element is a basic
    piece of information on the page, e.g. heading, table, selection input
    element...
    """

    def __init__(self, name: str, type: str):
        """Base class for all elements with counterparts in the frontend.

        Args:
            name (str): name of the element, unique identifier of the element
                in the component. If you name multiple components the same,
                the library appends number after the element.
            type (str): string that matches the backend element to the
                frontend element.
        """
        super().__init__(name)
        self._type = type
        self.changed = True

    @property
    def type(self):
        return self._type

    def construct_element_description(self) -> Dict[str, Any]:
        """Construct description of all the parts of the element to be
        displayed on the frontend.

        Sets changed to false!
        """
        self.changed = False
        return dict(
            name=self.name,
            type=self.type,
            **self.construct_element_configuration(),
        )

    @abstractmethod
    def construct_element_configuration(self) -> Dict[str, Any]:
        pass

    def register_to_server(self, server: Server):
        """
        Register the element's endpoint to the application

        Args:
            server (Server): the server to which the element is registered.
        """
        # by default nothing is registered
        pass

    def register_to_component(self, component: ComponentBase):
        """Registers the element to the component by ensuring
        that there isn't any other element which has the same name
        and if there is, change the name of this element by appending
        a number after it (e.g. naming the elements with the same name
        in order of registration to the component `c`, `c_1`, `c_2`, `c_3`,
        ...)
        """
        register_named(
            self, component.registered_element_names, component.registered_elements
        )


class ElementWithEndpoint(ElementBase):
    def __init__(
        self,
        name: str,
        type: str,
        endpoint_url: Optional[str] = None,
    ):
        """Base class for all elements with counterparts in the frontend that
        can send data to the backend

        Args:
            name (str): name of the element, unique identifier of the element
                in the component. If you name multiple components the same,
                the library appends number after the element.
            type (str): string that matches the backend element to the
                frontend element.
            endpoint_url (str, optional): url of the endpoint that the
                frontend will call when communicating with this element. If
                it is None, then a sanitized version of `name` will be used.
        """
        super().__init__(name, type)
        if endpoint_url is None:
            endpoint_url = sanitize_url(self.name)
        self.endpoint_url = endpoint_url
        self.parent_component: Optional[ComponentBase] = None
        self._type = type
        """The component that holds all the other elements. This is set
        in `ComponentBase.register_elements`
        """

    @abstractmethod
    def endpoint_callback(self):
        """Method that is called when the frontend sends data to the backend."""
        pass

    def construct_element_description(self) -> Dict[str, Any]:
        return dict(
            name=self.name,
            type=self.type,
            address=self.endpoint_url.removeprefix("/"),
            **self.construct_element_configuration(),
        )

    def register_to_server(self, server: Server):
        """Register the element's endpoint to the server.

        Args:
            server (Server)
        """
        register_named(NamedWrapper(self, "endpoint_url"), server.registered_urls)
        server.add_endpoint(self.endpoint_url, self.endpoint_callback, methods=["POST"])

    def register_to_component(self, component: ComponentBase):
        super().register_to_component(component)
        register_named(
            NamedWrapper(self, "endpoint_url"), component.registered_url_endpoints
        )
        self.parent_component = component
