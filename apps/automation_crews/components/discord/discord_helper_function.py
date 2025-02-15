import discord


async def send_message(
    message: discord.Message, user_message: str, crew, gmail
) -> None:

    if not user_message:
        return

    is_private = user_message[0] == "?"

    if is_private:
        user_message = user_message[1:]
    try:
        async with message.channel.typing():
            response = await gmail.login_via_bitwarden()
            if "No unread emails" in response or "No Attachment" in response:
                chunks = [response[i : i + 2000] for i in range(0, len(response), 2000)]
                for chunk in chunks:
                    if is_private:
                        await message.author.send(chunk)
                    else:
                        await message.channel.send(chunk)

            elif "Something Went Wrong!" in response:
                chunks = [response[i : i + 2000] for i in range(0, len(response), 2000)]
                for chunk in chunks:
                    if is_private:
                        await message.author.send(chunk)
                    else:
                        await message.channel.send(chunk)

            else:
                crew_response = str(crew.run_finance_crew())
                response = (
                    response
                    + "\n\n"
                    + "------------------------"
                    + "\n"
                    + crew_response
                )

                chunks = [response[i : i + 2000] for i in range(0, len(response), 2000)]

                for chunk in chunks:
                    if is_private:
                        await message.author.send(chunk)
                    else:
                        await message.channel.send(chunk)
    except Exception as e:
        print(f"An error occurred while sending a message: {e}")


async def run_finance_crew(
    message: discord.Message, user_message: str, crew, gmail
) -> None:

    if not user_message:
        return

    is_private = user_message[0] == "?"

    if is_private:
        user_message = user_message[1:]
    try:
        crew_response = str(crew.run_finance_crew())
        response = crew_response
        chunks = [response[i : i + 2000] for i in range(0, len(response), 2000)]
        for chunk in chunks:
            if is_private:
                await message.author.send(chunk)
            else:
                await message.channel.send(chunk)
    except Exception as e:
        print(f"An error occurred while sending a message: {e}")


async def run_invoice_crew(
    message: discord.Message, user_message: str, invoice_crew
) -> None:

    if not user_message:
        return

    is_private = user_message[0] == "?"

    if is_private:
        user_message = user_message[1:]
    try:
        crew_response = str(invoice_crew.run_invoice_crew())
        response = crew_response
        chunks = [response[i : i + 2000] for i in range(0, len(response), 2000)]
        for chunk in chunks:
            if is_private:
                await message.author.send(chunk)
            else:
                await message.channel.send(chunk)
    except Exception as e:
        print(f"An error occurred while sending a message: {e}")


async def run_dev_crew(
    message: discord.Message, user_message: str, WebsiteDevCrew
) -> None:

    if not user_message:
        return

    is_private = user_message[0] == "?"

    if is_private:
        user_message = user_message[1:]
    try:
        website_crew = WebsiteDevCrew(project_description=user_message)
        crew_response = website_crew.run()
        response = crew_response
        chunks = [response[i : i + 2000] for i in range(0, len(response), 2000)]
        for chunk in chunks:
            if is_private:
                await message.author.send(chunk)
            else:
                await message.channel.send(chunk)
    except Exception as e:
        print(f"An error occurred while sending a message: {e}")


async def train_finance_crew(
    message: discord.Message, user_message: str, crew, gmail
) -> None:

    if not user_message:
        return

    is_private = user_message[0] == "?"

    if is_private:
        user_message = user_message[1:]
    try:
        response = await crew.train_crew()
        await message.author.send(response)
    except Exception as e:
        print(f"An error occurred while sending a message: {e}")
