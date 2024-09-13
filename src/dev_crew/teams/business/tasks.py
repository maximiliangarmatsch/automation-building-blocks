from textwrap import dedent

from crewai import Task, Agent


class BusinessTasks:
    def __init__(self, project_description, output_directory):
        self.project_description = project_description
        self.output_directory = output_directory

    def prepare_document(self, agent: Agent) -> Task:
        return Task(
            description=dedent(
                f"""\
                    Your task is to develop a comprehensive product requirements document for the {self.project_description}. 
                    The document should include detailed specifications in the following areas:

                    1. **Color Schemes**: Define the color palette, including primary, secondary, and accent colors, 
                    as well as any branding guidelines that need to be followed.

                    2. **Frontend Pages**: Outline all the frontend pages that will be developed. For each page, include a 
                    description of its layout, navigation flow, and content details.

                    3. **Content Requirements**: Specify the types of content that need to be created or sourced, such as 
                    text, images, videos, etc.

                    4. **Backend APIs**: List all required backend APIs, detailing each endpoint, expected inputs, 
                    outputs, and any necessary authentication.

                    5. **API Responses**: Provide detailed descriptions of expected responses from the backend APIs, 
                    including the structure of success and error responses, status codes, and error messages.

                    Follow these instructions to ensure that all aspects of the project are thoroughly documented, 
                    which will guide the development team in delivering the project as per specifications.

                    Make sure to check with a human if the draft is good before finalizing your answer.
                """
            ),
            agent=agent,
            expected_output=dedent(
                """
                    A completed product requirements document that includes:

                    - A defined color scheme with branding guidelines.
                    - A list of all frontend pages with descriptions of their layout, navigation, and content.
                    - Detailed content requirements specifying the types of content needed.
                    - A comprehensive list of backend APIs with endpoints, inputs, outputs, and authentication details.
                    - Descriptions of expected API responses, including success and error cases with example structures.
            
                    The document should be clear, organized, and provide all necessary details to guide the development team.

                    Please check in the the human is you need any clarification.
            """
            ),
            human_input=True,
        )

    def define_product_vision_and_prioritize_features(self, agent: Agent) -> Task:
        return Task(
            title="Define Product Vision and Prioritize Features",
            description=dedent(
                """
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
            expected_goal=dedent(
                """
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
