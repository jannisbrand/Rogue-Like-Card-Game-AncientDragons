from typing import Type


class ECS_Context():
    def __init__(self):
        # ### ENTITIES AND COMPONENTS # ###
        self.entities: set[int]  # Collection of all id's
        # Mapping specific components mapped to entities to component types
        self.components: dict[Type, dict[int, any]]
        self.next_entity_id = 1
        self.number_of_registered_entities: int
        # ### ENTITIES AND COMPONENTS # ###

    def add_entity(self) -> int:
        """Creates a new entity in the context

        Returns:
            int: Id of the newly created entity
        """
        new_entity_id = self.next_entity_id
        self.entities.add(new_entity_id)
        self.next_entity_id += 1
        self.number_of_registered_entities += 1
        return new_entity_id

    def add_component(self, entity: int, component: any) -> None:
        """Mapps an instance of a component to an entity.

        Args:
            entity (int): The id of the entity
            component (instance): An instance of an component class
        """
        component_type = type(component)

        if component_type not in self.components:
            # Creates a new dictionary for a missing component type
            self.components[component_type] = {}    # This!

        self.components[component_type][entity] = component

    def get_components(self, entity: int) -> list[any]:
        """Returns a list of components

        Args:
            entity (int): The id of the entity

        Returns:
            list[any]: A list of component classes. 
            Returns [] if there are none.
        """
        components_of_entity = list()
        for component_type in self.components:
            try:
                component = self.components[component_type][entity]
                components_of_entity.append(component)
            except KeyError as e:
                print(f"[ECS]ECS_Context.get_components: {e}")
                print(f"[ECS]No entity found with component type: {component_type}!")
                continue
        return components_of_entity
