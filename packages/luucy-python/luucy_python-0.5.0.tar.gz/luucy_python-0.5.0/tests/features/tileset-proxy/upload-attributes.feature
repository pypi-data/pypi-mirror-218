Feature: Upload Attributes

  Uploading sttributes to existing 3D building layers

  Scenario: Update existing attribute

    Given that I have a valid layer ID, building UUID and attribute name
    When updating the attribute
    Then the data is saved
