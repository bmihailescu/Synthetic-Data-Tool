Feature: Synthetic data main home page

  Scenario Outline: Generate an ID data column with <record_count> records
    Given I can navigate to the Syn Data Home Page and create a CSV file with <record_count> ID's

    Examples:
      | record_count |
      | 10           |

  Scenario Outline: Generate an Address data column with <record_count> records
    Given I can navigate to the Syn Data Home Page and create a CSV file with <record_count> Address values

    Examples:
      | record_count |
      | 10           |

  Scenario Outline: Generate a Date data column with <record_count> records
    Given I can navigate to the Syn Data Home Page and create a CSV file with <record_count> Date values

    Examples:
      | record_count |
      | 10           |

  Scenario Outline: Generate an Email data column with <record_count> records
    Given I can navigate to the Syn Data Home Page and create a CSV file with <record_count> Email values

    Examples:
      | record_count |
      | 10           |

  Scenario Outline: Generate a Job data column with <record_count> records
    Given I can navigate to the Syn Data Home Page and create a CSV file with <record_count> Job values

    Examples:
      | record_count |
      | 10           |

  Scenario Outline: Generate Multiple Choice data with <record_count> records
    Given I can navigate to the Syn Data Home Page and create a CSV file with <record_count> Multiple Choice values

    Examples:
      | record_count |
      | 10           |

  Scenario Outline: Generate a Name data column with <record_count> records
    Given I can navigate to the Syn Data Home Page and create a CSV file with <record_count> Name values

    Examples:
      | record_count |
      | 10           |

  Scenario Outline: Generate a Number data column with <record_count> records
    Given I can navigate to the Syn Data Home Page and create a CSV file with <record_count> Number values

    Examples:
      | record_count |
      | 10           |

  Scenario Outline: Generate a String data column with <record_count> records
    Given I can navigate to the Syn Data Home Page and create a CSV file with <record_count> String values

    Examples:
      | record_count |
      | 10           |

  Scenario Outline: Generate a Text data column with <record_count> records
    Given I can navigate to the Syn Data Home Page and create a CSV file with <record_count> Text values

    Examples:
      | record_count |
      | 10           |