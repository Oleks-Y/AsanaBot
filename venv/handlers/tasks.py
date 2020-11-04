from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from misc import dp
from misc import bot
from Models.Asana import AsanaWorker
from colorama import Fore
from DatabaseWorker import DatabaseWorker

class TasksCreationStates(StatesGroup):
    waiting_for_command = State()
    waiting_for_task_name = State()
    waiting_for_option = State()


class TaskCreationWithFileStates(StatesGroup):
    waiting_for_option = State()


# token must be in the config
DEFAULT_PROJECT = "Closed "
asana = AsanaWorker("1/1198912032764129:365f64489d324a2f4ebb6e1329291d8a", DEFAULT_PROJECT)
dbWorker =DatabaseWorker()
available_file_options = ["1", "2", "3"]
available_task_create_options = ["First", "Second", "Third"]

@dp.message_handler(commands=['get_tasks'])
async def command_get_tasks(message: types.Message):
    await message.answer("Later there will be tasks")


@dp.message_handler(commands=["createtask"], state="*")
async def command_create_task(message: types.Message):
    await message.answer("Ok!Send me name of task now")
    await TasksCreationStates.waiting_for_task_name.set()


@dp.message_handler(state=TasksCreationStates.waiting_for_task_name, content_types=types.ContentTypes.TEXT)
async def create_task_get_name(message: types.Message, state: FSMContext):

    try:
        await state.update_data(taskText=message.text)
        # asana.create_task_with_name(message.text)
        keyboard = types.InlineKeyboardMarkup()
        for option in available_task_create_options:
            keyboard.add(types.InlineKeyboardButton(option, callback_data=option))
        await message.answer("Choose option", reply_markup=keyboard)
        await TasksCreationStates.waiting_for_option.set()
    except e:
        print(Fore.RED + e)


@dp.callback_query_handler(state=TasksCreationStates.waiting_for_option)
async def create_task_callback(callback_query: types.CallbackQuery, state: FSMContext):
    task_text = (await state.get_data())["taskText"]
    choosen_option = callback_query.data
    asigneeName = ""
    if choosen_option == "First":
        asiignee_gid = asana.getUserId("Oleksandr")
        asigneeName="Oleksandr"
    elif choosen_option == "Second":
        asiignee_gid = asana.getUserId("Alex")
        asigneeName="Alex"
    elif choosen_option == "Third":
        asiignee_gid = asana.getUserId("Alex")
        asigneeName="Alex"
    # get file
    task_gid = asana.create_task_with_name_and_asignee(name=task_text, assignee_gid=asiignee_gid)
    dbWorker.createTask(task_text, asigneeName)
    # await callback_query.answer("Created!")
    await bot.send_message(callback_query.message.chat.id, "Created!")
    await callback_query.message.delete()
    await state.finish()
@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def start_creating_task_with_file(message: types.Message, state: FSMContext):
    # send reply markup
    # save doc in state
    await state.update_data(file_to_send=message.document)
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard = types.InlineKeyboardMarkup()
    for option in available_file_options:
        keyboard.add(types.InlineKeyboardButton(option, callback_data=option))
    await message.answer("Choose option", reply_markup=keyboard)
    await TaskCreationWithFileStates.waiting_for_option.set()



@dp.message_handler(state=TaskCreationWithFileStates.waiting_for_option)
async def create_with_option(message: types.Message, state: FSMContext):
    # get document
    # get option
    asiignee_gid = ""
    choosen_option = message.text
    if choosen_option == "1":
        asiignee_gid = asana.getUserId("Oleksandr")
    elif choosen_option == "2":
        asiignee_gid = asana.getUserId("Alex")
    elif choosen_option == "3":
        asiignee_gid = asana.getUserId("Alex")
    fileObj = await state.get_data()
    # get file
    file_path = (await bot.get_file(fileObj["file_to_send"]["file_id"]))["file_path"]
    file = await bot.download_file(file_path)
    task_gid = asana.create_task_with_name_and_asignee(name=choosen_option, assignee_gid=asiignee_gid)["gid"]
    asana.attach_file_to_task(file, task_gid, fileObj["file_to_send"]["file_name"])
    await message.answer("Created !", reply_markup=types.ReplyKeyboardRemove(), )
    await state.finish()


@dp.callback_query_handler(state=TaskCreationWithFileStates.waiting_for_option)
async def create_with_option_callbck(callback_query: types.CallbackQuery, state: FSMContext):
    asiignee_gid = ""
    choosen_option = callback_query.data
    asigneeName=""
    nameOfTask = ""
    if choosen_option == "1":
        asiignee_gid = asana.getUserId("Oleksandr")
        asigneeName = "Oleksandr"
        nameOfTask = "4"
    elif choosen_option == "2":
        asiignee_gid = asana.getUserId("Alex")
        asigneeName = "Alex"
        nameOfTask = "4"
    elif choosen_option == "3":
        asiignee_gid = asana.getUserId("Alex")
        asigneeName = "Alex"
        nameOfTask = "4"
    fileObj = await state.get_data()
    # get file
    file_path = (await bot.get_file(fileObj["file_to_send"]["file_id"]))["file_path"]
    file = await bot.download_file(file_path)
    task_gid = asana.create_task_with_name_and_asignee(name=nameOfTask, assignee_gid=asiignee_gid)["gid"]
    dbWorker.createTask(choosen_option,asigneeName )
    asana.attach_file_to_task(file, task_gid, fileObj["file_to_send"]["file_name"])
    # await message.answer("Created !")
    # await state.finish()
    await state.finish()
    # await callback_query.answer("Created!")
    await bot.send_message(callback_query.message.chat.id, "Created!")
    await callback_query.message.delete()
