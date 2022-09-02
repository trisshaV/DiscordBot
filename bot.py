import lightbulb
import hikari

bot = lightbulb.BotApp(token='', default_enabled_guilds=(656434422199091221))    # With guild id's, slash commands will be registered quicker

@bot.listen(hikari.StartedEvent)
async def on_start(event):
    print('Bot has started')

# The order these decorators appear before each other is IMPORTANT
@bot.command
@lightbulb.command('ping', 'Says pong!')
@lightbulb.implements(lightbulb.SlashCommand) # Slash commands
async def ping(ctx):    #context object
    await ctx.respond('Pong!')
    
@bot.command
@lightbulb.command('group', 'This is a group')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def my_group(ctx):
    pass

@my_group.child        # Subcommand
@lightbulb.command('subcommand', 'This is a subcommand')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommand(ctx):
    await ctx.respond('I am a subcommand')
    
@bot.command
@lightbulb.option('num1', 'The first number', type=int)
@lightbulb.option('num2', 'The second number', type=int) # must be above command decorator
@lightbulb.command('add', 'Add two numbers together')
@lightbulb.implements(lightbulb.SlashCommand)
async def add(ctx):
    await ctx.respond(ctx.options.num1 + ctx.options.num2)

bot.run()