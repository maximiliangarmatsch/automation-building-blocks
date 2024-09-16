from textwrap import dedent

from crewai import Task, Agent


def write_content_task(agent: Agent, project_description: str) -> Task:
    return Task(
        description=dedent(
            f"""
            Write engaging, informative, and SEO-optimized content for the {project_description}. 
            The content should be tailored to the target audience, aligning with the brand's tone 
            and messaging. Ensure that each piece of content drives user engagement and contributes 
            to the overall user experience on the website.

            The task involves:
            - Writing compelling copy for all key pages of the website (e.g., homepage, about page, 
              product pages, blog, etc.).
            - Optimizing each page's content with relevant keywords to improve search engine rankings.
            - Crafting concise and persuasive product descriptions that highlight the key benefits 
              and features.
            - Ensuring a consistent tone and style throughout the site that aligns with the brand's 
              voice.
            - Collaborating with the design team to ensure content complements the visual elements 
              of the site.
            """
        ),
        agent=agent,
        expected_output=dedent(
            """
            - Written content for all pages of the website, including:
                - SEO-optimized text for key landing pages, product descriptions, and blog posts.
                - Keyword-optimized headings, subheadings, and meta descriptions for better search 
                  engine visibility.
                - Clear and persuasive product descriptions that drive user interest and conversions.
                - Consistent, brand-aligned tone and messaging across all website pages.
                - Documentation of the content creation process, including keyword research and 
                  engagement strategies.
            """
        ),
    )
