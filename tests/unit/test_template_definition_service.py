import unittest
from unittest.mock import MagicMock, create_autospec
from src.services.template_definition_service import TemplateDefinitionService
from src.repositories.template_definition_repository import TemplateDefinitionRepository
from src.entities.template_definition import TemplateDefinition
from sqlalchemy.orm import Session

class TestTemplateDefinitionService(unittest.TestCase):
    def setUp(self):
        self.mock_session = create_autospec(Session)
        self.mock_template_definition_repository = MagicMock(spec=TemplateDefinitionRepository(self.mock_session))
        self.template_definition_service = TemplateDefinitionService(self.mock_session)
        self.template_definition_service.template_definition_repository = self.mock_template_definition_repository

    def test_create(self):
        # Arrange
        template = TemplateDefinition(uuid="id", name="name", description="description", template_body="{}")
        self.mock_template_definition_repository.create.return_value = template
        # Act
        result = self.template_definition_service.create(template)
        # Assert
        self.mock_template_definition_repository.create.assert_called_once_with(template)
        self.assertEqual(result, template)
