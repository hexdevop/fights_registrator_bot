from aiogram import Dispatcher

from . import (
    main,
    registration,
)


def reg_packages(dp: Dispatcher):
    packages = [
        main,
        registration,
    ]
    for package in packages:
        package.reg_routers(dp)
