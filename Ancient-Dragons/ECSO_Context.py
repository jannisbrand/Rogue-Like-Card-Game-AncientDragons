from typing import Type, Any

from Characters import Base

"""
TODO:
    - Für die Typen der Komponenten entscheiden.
        -> Was sind sie? (Klasse; Struct; ...; ...)
        -> Wie sind sie strukturiert?

    - Für den "Speicher-Ort" der Komponenten entscheiden.
        -> Die SQL-Datenbank? (Macht aber eigentlich keinen Sinn! Instanzen und so..)
        -> Eigene Text-/Python-File?
        -> Oder was ganz anderes?

    - Die Komponenten definieren.
        -> Die Karteneigenschaften zu ECS-Komponenten übersetzen

-------------------------------------------------------------------------
    Grobe Beschreibung..
    
    Prozessbeginn:
    - Der Initiale Applikationstand wird hergestellt.
        -> Applikations Kontext wird erstellt.
        -> Event handler werden erstellt.
        -> ECS Kontext wird erstellt.
        -> Render Kontext wird erstellt.
        -> Entity Factory wird erstellt.

    - Die Entity Factory, bekommt/ließt die Karten-Daten aus der Datenbank.
        -> Entities werden erstellt
        -> Komponenten werden erstellt und den Entieties zugewiesen.

    - Der ECS Kontext, wird von der Entity Factory mit Karten gefüllt.
        -> Die erstellten Entities, sowie die alle erstellten Komponenten, die den Entities zugewiesen sind, sind hier.

    - Die Charakter Factory, bekommt/ließt die Daten aus der Datenbank.
        -> Die Charakter Klassen werden erstellt.
        -> Die Entity Id's, die den Standart-Karten der Charaktere entsprechen, werden den Klassen übergeben.

    Future:
    - Der Game Mode wird erstellt. (Wie genau ist die Frage.. Datenbank, oder einfach Hard-Code)
    - Die Level Factory bekommt/ließt die Daten aus der Datenbank.
        -> Mit einem statischen seed, wird mit dem Abschluss eines Levels ein weiteres generiert.
"""


class ECSO_Context():
    def __init__(self):
        # ### ENTITIES AND COMPONENTS # ###
        self.entities: set[int] = set() # Collection of all id's
        # Mapping specific components mapped to entities to component types
        self.components: dict[Type, dict[int, list[Any]]] = {}
        self.next_entity_id = 1
        self.number_of_registered_entities: int = 0
        # ### ENTITIES AND COMPONENTS # ###

        # ### OBJECTS ### #
        self.objects: dict[str, list[Any]] = {}
        self.next_object_id = 1
        # ### OBJECTS ### #

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

    def add_component(self, entity: int, component: Any) -> None:
        """Mapps an instance of a component to an entity.

        Args:
            entity (int): The id of the entity
            component (instance): An instance of an component class
        """
        component_type = type(component)

        if component_type not in self.components:
            # Creates a new dictionary for a missing component type
            self.components[component_type] = {}    # This!

        if entity not in self.components[component_type]:
            self.components[component_type][entity] = []

        print(self.components[component_type][entity])
        self.components[component_type][entity].append(component)

    def add_components(self, entity: int, components: list[Any]) -> None:
        """Mapps an instance of a component to an entity.

        Args:
            entity (int): The id of the entity
            component (instance): An instance of an component class
        """
        for component in components:
            component_type = type(component)

            if component_type not in self.components:
                # Creates a new dictionary for a missing component type
                self.components[component_type] = {}    # This!
            
            if entity not in self.components[component_type]:
                self.components[component_type][entity] = []

            self.components[component_type][entity].append(component)

    def get_components(self, entity: int) -> list[Any]:
        """Returns a list of components

        Args:
            entity (int): The id of the entity

        Returns:
            list[any]: A list of component classes. 
            Returns [] if there are none.
        """
        components_of_entity = []
        for component_type in self.components:
            try:
                components = self.components[component_type][entity]
                components_of_entity.extend(components)
            except KeyError as e:
                print(f"[ECSOContext]No entity found with component type: {e}!")
                continue
        return components_of_entity

    def add_object(self, type: str, object: Any) -> None:
        try:
            if type not in self.objects:
                self.objects[type] = []

            self.objects[type].append(object)
            self.next_object_id += 1
        except KeyError as e:
            print(f"[ECSOContext] Object could not be added: {e}")

    def add_objects(self, type: str, objects: list[Any]) -> None:
        try:
            for object in objects:
                self.add_object(type, object)  # Smart :)
        except KeyError as e:
            print(f"[ECSOContext] Objects could not be added: {e}")

    def get_objects(self, type: str) -> list[Any]:
        return self.objects[type]

    def get_object(self, type: str, id: int) -> Any:
        try:
            for object in self.objects[type]:
                if object.id == id:
                    return object
        except KeyError as e:
            print(f"[ECSOContext] Object could not be gotten?: {e}")
