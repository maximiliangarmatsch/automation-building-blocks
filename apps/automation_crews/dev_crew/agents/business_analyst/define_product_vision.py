from textwrap import dedent

from crewai import Task, Agent


def define_product_vision(agent: Agent) -> Task:
    return Task(
        description=dedent(
            """\
            Your task is to define the product vision and prioritize features for the project. 
            The document should include:

            1. **Product Vision**: Articulate a clear product vision that aligns with the project goals and stakeholder expectations. 
               The vision should capture the essence of what the product aims to achieve and its value proposition to the users.

            2. **Feature List**: Compile a comprehensive list of features that are necessary for the project. This list should be 
               detailed enough to guide the development team and include any key functionalities that are critical to the product’s success.

            3. **Feature Prioritization**: Prioritize the features using a suitable framework (e.g., MoSCoW, RICE, or Value vs. Complexity). 
               Justify the prioritization decisions to ensure alignment with business goals and technical feasibility.

            4. **User Stories**: For each prioritized feature, create user stories that describe the functionality from the user’s perspective. 
               Include acceptance criteria that clearly define when a feature is considered complete and functioning as expected.

            5. **Roadmap Recommendations**: Provide recommendations for a high-level product roadmap that outlines the phased implementation 
               of features. This roadmap should reflect the priorities and any dependencies among the features.

            Ensure that the document provides clear and actionable guidance for the project team to deliver maximum value.
            """
        ),
        expected_output=dedent(
            """\
            A completed product vision and feature prioritization document that includes:

            - A well-defined product vision statement that captures the project’s goals and value proposition.
            - A comprehensive list of features, prioritized according to business value and feasibility.
            - User stories with acceptance criteria for each prioritized feature.
            - High-level recommendations for a product roadmap that outlines phased implementation.

            The document should be clear, detailed, and aligned with the overall project objectives, providing a strong foundation 
            for guiding the development team.
            """
        ),
        agent=agent,
        allow_delegation=False,
    )
