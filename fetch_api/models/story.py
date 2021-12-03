from neomodel import (
    StringProperty,
    StructuredNode,
    RelationshipTo,
    IntegerProperty,
    FloatProperty,
    BooleanProperty
)


class Story(StructuredNode):
    # Properties
    nodeID = IntegerProperty(index=True, db_property='id')
    sentimentScore = StringProperty()
    sentiment = StringProperty()
    notes = StringProperty()
    name = StringProperty()
    value = StringProperty()
    acceptance_criteria = StringProperty()
    complexity = IntegerProperty()
    priority = FloatProperty()
    approved = BooleanProperty()

    # Relationships
    requires = RelationshipTo('.story.Story', 'REQUIRES')
