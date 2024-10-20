from textwrap import dedent

from crewai import Task, Agent


def integrate_and_test(agent: Agent) -> Task:
    return Task(
        description=dedent(
            """
            Integrate the frontend and backend components of the website to ensure 
            seamless communication between the two. This includes verifying that all 
            API endpoints are functioning correctly and the data is properly passed 
            between the frontend and backend.

            Once the integration is complete, perform thorough testing of the entire 
            website. This should include:
            - Functional testing to verify that all features are working as expected.
            - Cross-browser testing to ensure the site performs consistently across 
              major browsers (Chrome, Firefox, Safari, Edge).
            - Responsiveness testing across different devices (desktop, tablet, mobile).
            - Performance testing to ensure fast load times and optimal user experience.
            - Security testing to identify and mitigate potential vulnerabilities.
            
            Document any issues encountered during the integration and testing phases, 
            and collaborate with the development team to resolve them. Re-test any 
            areas affected by fixes or updates.
            """
        ),
        agent=agent,
        expected_output=dedent(
            """
            - A detailed test report that includes:
                - Results from functional, cross-browser, responsiveness, performance, 
                  and security testing.
                - Any identified issues during integration or testing, including 
                  descriptions and severity.
                - Confirmation of successful integration of the frontend and backend.
                - Steps taken to resolve any issues, with re-testing results.
            """
        ),
    )
