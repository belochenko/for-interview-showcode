from wasabi import msg


async def on_startup(dp):
    msg.good("Bot started successfully!")
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)
    from utils.setup_commands import on_startup_commands
    await on_startup_commands(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    msg.info("Trying to start bot...")
    executor.start_polling(dp, on_startup=on_startup)
