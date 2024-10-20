from textwrap import dedent

from crewai import Task, Agent


def develop_frontend(
    agent: Agent, output_directory: str
) -> Task:
    return Task(
        description=dedent(
            f"""
                Read the requirements in {output_directory}/docs/frontend_requirements.txt and
                implement the frontend application using Reactjs and tailwindcss.
                Also, incorporate the backend requirements from {output_directory}/docs/backend_requirements.txt into the app.
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
                
                Save all files in the {output_directory}/frontend folder.

                RULES
                -----
                - Make sure to build a fully functional app and write a README on how to start the application you made.
                - DO NOT use a generic README that doesn't relate specifically to the app you created. The README should be enough to start and test the application you created. 
                - NEVER USE Apostrophes for contraction!
                - keep the same style and tailwind classes.
                - ALL COMPONENTS USED SHOULD BE IMPORTED, don't make up components.

                If you follow the rules I'll give you a $100 tip!!! 
                MY LIFE DEPEND ON YOU FOLLOWING IT!
            """
        ),
        agent=agent,
        expected_output=dedent(
            f"""
                - All necessary frontend files for each page, including reusable components, 
                  saved in the {output_directory}/frontend folder.
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
