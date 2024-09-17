from textwrap import dedent

from crewai import Task, Agent


def prepare_document(
    agent: Agent, project_description: str, output_directory: str
) -> Task:
    output_directory = output_directory + "/docs"
    return Task(
        description=dedent(
            f"""\
                    Your task is to develop a comprehensive product requirements document for the {project_description}. 
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

                    Create only these files:
                    1. frontend_requirements.txt - to contain all frontend pages, color schemes, content requirements and all necessary information.
                    2. backend_requirements.txt - to contain all backend apis, api responses and all necessary information to help the backend function effectively and efficiently.

                    Each file should be well documented and simple so other crews can pick them and work on them easily.

                    Save all files in the {output_directory} folder.
                """
        ),
        agent=agent,
        expected_output=dedent(
            """\
                    Neccessary files saved in the {self.output_directory} folder

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
