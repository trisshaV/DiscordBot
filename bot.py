import hikari

bot = hikari.GatewayBot(token='MTAxNDUxNDUzNTc5NDc0OTU4Mg.Gk09R4.fE20U-UlfiED8oMFyCgYBo4pc9gvFK_RH37To0')

@bot.listen(hikari.GuildMessageCreateEvent)
async def print_message(event):
    print(event.content)

@bot.listen(hikari.StartedEvent)
async def bot_started(event):
    print('Bot has started!')
    
bot.run()