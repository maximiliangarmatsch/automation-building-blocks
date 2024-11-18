from GPTdiscord.utils.helpers.image_analysis_helper import (
    encode_discord_image,
    analyze_image,
)
from GPTdiscord.utils.helpers.openai_message_format_helper import format_error_message


async def image_analyzer(ctx):

    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]

        if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            async with ctx.typing():

                try:
                    base64_image = await encode_discord_image(attachment.url)
                    instructions = "Please describe the image."
                    analysis_result = await analyze_image(base64_image, instructions)
                    response_text = (
                        analysis_result.get("choices", [{}])[0]
                        .get("message", {})
                        .get("content", "")
                    )

                    if response_text:
                        await ctx.send(response_text)
                    else:
                        await ctx.send("Sorry, I couldn't analyze the image.")

                except Exception as e:
                    error_details = str(e)
                    if hasattr(e, "response") and e.response is not None:
                        error_details += f" Response: {e.response.text}"
                    formatted_error = format_error_message(error_details)
                    await ctx.send(formatted_error)
    else:
        await ctx.send("Please attach an image to analyze.")
