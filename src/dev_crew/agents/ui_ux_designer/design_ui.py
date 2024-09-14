from textwrap import dedent

from crewai import Task, Agent


def design_ui_task(agent: Agent, project_description: str) -> Task:
    return Task(
        description=dedent(
            f"""
            Design the user interface (UI) for the {project_description}. 
            The design should include layouts for all key pages, ensuring consistency 
            across the entire site. Focus on creating an intuitive, user-friendly interface 
            that aligns with the project’s goals and target audience.

            The task involves:
            - Creating wireframes for each page, starting from low-fidelity sketches 
              and progressing to shigh-fidelity prototypes.
            - Defining the color schemes, typography, and visual style to maintain 
              brand identity and appeal.
            - Designing key components like navigation bars, buttons, forms, and 
              interactive elements that are both functional and visually appealing.
            - Incorporating user feedback to iterate on the design and ensure 
              usability and accessibility.

            Additionally, generate a sample image of the main interface to give 
            a visual preview of the design. Before finalizing, ensure to check 
            with a human for feedback on the draft to refine the design further 
            based on real-world insights and preferences.
            """
        ),
        agent=agent,
        expected_output=dedent(
            """
            - Detailed UI design specifications, including:
                - High-fidelity wireframes and mockups for all key pages.
                - A comprehensive style guide outlining the color palette, typography, 
                  and UI components used.
                - Descriptions of user flows for the primary actions (e.g., sign-up, 
                  checkout, search).
            - A sample image of the main interface, demonstrating the overall look and feel.
            - Documentation of any iterations made based on human feedback.
            """
        ),
        human_input=True,
    )
