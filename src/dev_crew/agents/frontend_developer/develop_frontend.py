from textwrap import dedent

from crewai import Task, Agent


def develop_frontend(
    agent: Agent, output_directory: str
) -> Task:
    return Task(
        description=dedent(
            f"""
                Read the requirements in {output_directory}/docs/frontend_requirements.txt and
                implement the application for using React, 
                TailwindCSS, and/or any necessary tools to ensure a clean, functional, 
                and responsive frontend. Focus on creating modular, reusable components 
                that follow best practices for maintainability and scalability. Ensure 
                accessibility (a11y) and web performance optimization are part of the 
                development process. 

                Use modern JavaScript/TypeScript conventions and ensure the project 
                is structured properly with well-organized files and folders, 
                keeping separation of concerns in mind (e.g., separating logic, UI components, 
                and styles). Implement error handling where appropriate, and ensure that 
                the frontend integrates seamlessly with any APIs or backend services.
                
                Save all files in the {output_directory} folder.
            """
        ),
        agent=agent,
        expected_output=dedent(
            f"""
                - All necessary frontend files for each page, including reusable components, 
                  saved in the {output_directory} folder.
                - A clearly structured codebase, with separation of concerns between UI, 
                  logic, and styles.
                - Use of performance best practices such as lazy loading, code splitting, 
                  and minified assets.
                - All components and pages should follow accessibility standards and 
                  include proper semantic HTML tags.
                - Integration with any backend services or APIs should be functional 
                  and error handling should be in place for failed requests.
                - A README.md file detailing step-by-step instructions to install, 
                  build, and run the application locally, including any dependencies 
                  and environment setup.
                - Testing for critical components and logic, with unit or integration tests 
                  where applicable.
                - TailwindCSS should be used efficiently, leveraging utility classes to 
                  minimize the need for custom CSS, while keeping the design clean 
                  and responsive.
            """
        ),
    )
