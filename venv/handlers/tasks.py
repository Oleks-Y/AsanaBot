from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from misc import dp
from misc import bot
from Models.Asana import AsanaWorker
from colorama import Fore


class TasksCreationStates(StatesGroup):
    waiting_for_command = State()
    waiting_for_task_name = State()
class TaskCreationWithFileStates(StatesGroup):
    waiting_for_option = State()
# token must be in the config
asana = AsanaWorker("1/1198912032764129:365f64489d324a2f4ebb6e1329291d8a")

available_file_options = ["1", "2","3"]
@dp.message_handler(commands=['get_tasks'])
async def command_get_tasks(message : types.Message) :
    await message.answer("Later there will be tasks")

@dp.message_handler(commands=["createtask"],state="*")
async def command_create_task(message : types.Message ) :
    await message.answer("Ok!Send me name of task now")
    await TasksCreationStates.waiting_for_task_name.set()

@dp.message_handler(state=TasksCreationStates.waiting_for_task_name, content_types=types.ContentTypes.TEXT)
async def create_task_get_name(message: types.Message, state: FSMContext):
    await message.answer("Ok!I`m creating task now!")
    try:
        asana.create_task_with_name(message.text)
        TasksCreationStates.next()
    except e :
        print(Fore.RED +e)

@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def start_creating_task_with_file(message: types.Message, state: FSMContext):
    # send reply markup
    # save doc in state
    await state.update_data(file_to_send=message.document)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for option in available_file_options:
        keyboard.add(option)
    await message.answer("Choose option", reply_markup=keyboard)
    await TaskCreationWithFileStates.waiting_for_option.set()
@dp.message_handler(state=TaskCreationWithFileStates.waiting_for_option)
async def create_with_option(message : types.Message, state: FSMContext):
    # get document
    # get option
    choosen_option  = message.text
    fileObj = await state.get_data()
    # get file
    file_path = (await bot.get_file(fileObj["file_to_send"]["file_id"]))["file_path"]
    file = await bot.download_file(file_path)
    task_gid = asana.create_task_with_name(name=choosen_option)["gid"]
    asana.attach_file_to_task(file, task_gid, fileObj["file_to_send"]["file_name"])
    await message.answer("Created !",reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

