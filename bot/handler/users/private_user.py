import os
import asyncio
import django
from datetime import datetime
from aiogram import Router,F
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandStart
from aiogram.types import Message,CallbackQuery

from asgiref.sync import sync_to_async
from set_main.models import UserCreate,BotButtonInline,CreateTest,BotToken,UserResult
from ...filters.chat_type import chat_type_filter,send_bot_message,CreateInline,CheckSubChanel,CheckSubChanelCall
from ...states.user_state import UserStates

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

user_private_router = Router()
user_private_router.message.filter(
    chat_type_filter(['private']),
    CheckSubChanel(),
    CheckSubChanelCall(),
)

now_date = datetime.now()

@user_private_router.message(CommandStart())
async def private_start(message:Message,state:FSMContext):
    user_id = message.from_user.id
    user = await sync_to_async(UserCreate.objects.filter(telegram_id=user_id).first)()
    if user:
        await send_bot_message(message.bot,user_id,'start')
    else:
        message_id = await send_bot_message(message.bot,user_id,'full_name')
        await state.set_state(UserStates.full_name)
        await state.update_data(name_id=message_id)

@user_private_router.callback_query(F.data=='chanel_sub',CheckSubChanelCall(),)
async def admin(call:CallbackQuery,state:FSMContext):
    user_id = call.from_user.id
    user = await sync_to_async(UserCreate.objects.filter(telegram_id=user_id).first)()
    if user:
        await send_bot_message(call.message.bot,user_id,'start')
    else:
        await send_bot_message(call.message.bot,user_id,'full_name')
        await state.set_state(UserStates.full_name)

@user_private_router.callback_query(F.data=='admin',CheckSubChanelCall())
async def admin(call:CallbackQuery):
    admin = await sync_to_async(BotToken.objects.filter(user='Admin').first)()
    buttons_data = await sync_to_async(list)(BotButtonInline.objects.filter(message__command='start'))
    await call.message.answer(f"Admin: {admin.user_url}",reply_markup=CreateInline(buttons_data) if buttons_data else '')
    await call.message.delete()

@user_private_router.callback_query(F.data=='settings',CheckSubChanelCall())
async def set_ting(call:CallbackQuery,state:FSMContext):
    user_id = call.from_user.id
    await send_bot_message(call.message.bot,user_id,'setting')
    await state.set_state(UserStates.main)
    await call.message.delete()
    
@user_private_router.callback_query(F.data=='name',UserStates.main,CheckSubChanelCall())
async def set_ting(call:CallbackQuery,state:FSMContext):
    user_id = call.from_user.id
    await send_bot_message(call.message.bot,user_id,'update_name')
    await state.set_state(UserStates.name)
    await call.message.delete()

@user_private_router.callback_query(F.data=='name_back',UserStates.name,CheckSubChanelCall())
async def set_ting(call:CallbackQuery,state:FSMContext):
    user_id = call.from_user.id
    await send_bot_message(call.message.bot,user_id,'setting')
    await state.set_state(UserStates.main)
    await call.message.delete()

@user_private_router.message(F.text,UserStates.name)
async def name(message:Message,state:FSMContext):
    user_id = message.from_user.id
    name = message.text
    user = await sync_to_async(UserCreate.objects.filter(telegram_id=user_id).first)()
    if user:
        user.first_name = name
        await sync_to_async(user.save)()  # Сохраняем изменения в асинхронном режиме
        await send_bot_message(message.bot, user_id, 'start')
        await state.clear()
        await message.delete()
    else:
        await message.answer("Пользователь не найден.")

@user_private_router.callback_query(F.data=='last',UserStates.main,CheckSubChanelCall())
async def set_ting(call:CallbackQuery,state:FSMContext):
    user_id = call.from_user.id
    await send_bot_message(call.message.bot,user_id,'update_last')
    await state.set_state(UserStates.last)
    await call.message.delete()

@user_private_router.callback_query(F.data=='last_back',UserStates.last,CheckSubChanelCall())
async def set_ting(call:CallbackQuery,state:FSMContext):
    user_id = call.from_user.id
    await send_bot_message(call.message.bot,user_id,'setting')
    await state.set_state(UserStates.main)
    await call.message.delete()

@user_private_router.message(F.text,UserStates.last)
async def name(message:Message,state:FSMContext):
    user_id = message.from_user.id
    last = message.text
    if last.endswith('v') or last.endswith('a'):
        user = await sync_to_async(UserCreate.objects.filter(telegram_id=user_id).first)()
        if user:
            user.last_name = last
            await sync_to_async(user.save)()  # Сохраняем изменения в асинхронном режиме
            await send_bot_message(message.bot, user_id, 'start')
            await state.clear()
            await message.delete()
        else:
            await message.answer("Пользователь не найден.")
    else:
        await message.answer("familiyangizni kiriting\nBoltayev | Boltayeva")

@user_private_router.callback_query(F.data=='back',UserStates.main,CheckSubChanelCall())
async def set_ting(call:CallbackQuery,state:FSMContext):
    user_id = call.from_user.id
    await send_bot_message(call.message.bot,user_id,'start')
    await state.clear()
    await call.message.delete()

@user_private_router.callback_query(F.data=='check_answer',CheckSubChanelCall())
async def check(call:CallbackQuery,state:FSMContext):
    user_id = call.from_user.id
    await call.message.delete()
    message_id = await send_bot_message(call.message.bot,user_id,'send_code')
    await state.update_data(test_code=message_id)
    await state.set_state(UserStates.cod)

@user_private_router.callback_query(F.data=='send_back',UserStates.cod,CheckSubChanelCall())
async def set_ting(call:CallbackQuery,state:FSMContext):
    user_id = call.from_user.id
    await send_bot_message(call.message.bot,user_id,'start')
    await state.clear()
    await call.message.delete()

@user_private_router.message(F.text, UserStates.cod)
async def code(message: Message, state: FSMContext):
    data = await state.get_data()
    tst_code = data.get('test_code')
    user_id = message.from_user.id
    cod = message.text
    
    if tst_code:
        try:
            await message.bot.delete_message(chat_id=user_id, message_id=tst_code)
        except Exception as e:
            print(f"Error deleting message: {e}")

    if cod.isdigit():
        code = int(cod)
        
        # Получаем тест по коду
        test = await sync_to_async(CreateTest.objects.filter(cod=code).first)()
        
        if test:  # Проверяем, что тест найден
            # Проверяем, есть ли уже результат для пользователя и теста
            result = await sync_to_async(UserResult.objects.filter(user__telegram_id=user_id, test=test).first)()
            
            if result:
                await send_bot_message(message.bot, user_id, 'agin')
                return
            else:
                bot_text = {
                    'code': code,
                    'len': len(test.test),
                }
                text = test.test
                message_id = await send_bot_message(message.bot, user_id, 'exam', bot_text)
                await state.update_data(text_t=text, code=code,exam_id = message_id)
                await state.set_state(UserStates.answer)
                await message.delete()
        else:
            await send_bot_message(message.bot,user_id,'error_find')
    else:
        await send_bot_message(message.bot,user_id,'error_int')

@user_private_router.message(F.text, UserStates.answer)
async def answer(message: Message, state: FSMContext):
    data = await state.get_data()
    exam_id = data.get('exam_id')
    user_id = message.from_user.id
    code = data.get('code')
    test = data.get('text_t')
    answer = message.text
    
    if exam_id:
        try:
            await message.bot.delete_message(chat_id=user_id, message_id=exam_id)
        except Exception as e:
            print(f"Error deleting message: {e}")
    
    # Подготовка данных для проверки
    main_test = ''.join(i.upper() for i in test if not i.isdigit())
    filter_answer = ''.join(i.upper() for i in answer if not i.isdigit())
    
    if len(filter_answer) != len(main_test):
        await send_bot_message(message.bot,user_id,'error_len')
        return
    
    # Получение данных пользователя, теста и администратора
    admin, user, test_create = await asyncio.gather(
        sync_to_async(BotToken.objects.filter(user='Admin').first)(),
        sync_to_async(UserCreate.objects.filter(telegram_id=user_id).first)(),
        sync_to_async(CreateTest.objects.filter(cod=code).first)(),
    )

    # Проверка наличия необходимых данных
    if not user:
        await message.answer("Пользователь не найден.")
        return
    if not test_create:
        await message.answer("Тест не найден.")
        return

    correct = [actual for expected, actual in zip(filter_answer, main_test) if expected == actual]
    wrong = [actual for expected, actual in zip(filter_answer, main_test) if expected != actual]
    percent = len(correct) * 100 / len(main_test)

    # Создание результата теста
    await sync_to_async(UserResult.objects.create)(
        user=user,
        test=test_create,
        count_correct=len(correct),
        count_wrong=len(wrong),
        percent=percent,
        correct_str=''.join(correct),
        wrong_str=''.join(wrong)
    )

    # Формирование текста для отправки
    name, last = user.first_name, user.last_name
    date = f'{now_date.year}-{now_date.month}-{now_date.day}'
    hours = f'{now_date.hour}:{now_date.minute}'
    bot_text = {
        'name': name,
        'last': last,
        'code': code,
        'percent': percent,
        'date': date,
        'hour': hours,
        'url': admin.user_url if admin else "URL отсутствует"
    }
    if test_create.subject:
        bot_text['subject'] = test_create.subject
        await send_bot_message(message.bot, user_id, 'fan_result', bot_text)
    else:
        await send_bot_message(message.bot, user_id, 'simple_result', bot_text)
    await message.delete()    

@user_private_router.message(F.text, UserStates.full_name)
async def test(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    msg = data.get('name_id')
    
    if msg:
        try:
            await message.bot.delete_message(chat_id=user_id, message_id=msg)
        except Exception as e:
            print(f"Error deleting message: {e}")
    
    try:
        name_parts = message.text.split()

        if len(name_parts) != 2:
            raise ValueError("Expected two names")
        
        last_name, first_name = name_parts
        male = 'male' if last_name.endswith('v') else 'female'

        if not (last_name.endswith('v') or last_name.endswith('a')):
            raise ValueError("Invalid last name format")
        
        message_id = await send_bot_message(message.bot,user_id,'class')
        await state.update_data(first_name=first_name,last_name=last_name,male=male,class_id = message_id)
        await state.set_state(UserStates.classes)
        await message.delete()
    except ValueError:
        await send_bot_message(message.bot,user_id,'wrong_fullname')

@user_private_router.callback_query(F.data,UserStates.classes)
async def test(call:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    msg = data.get('class_id')
    user_id = call.from_user.id
    classes = call.data
    
    if msg:
        try:
            await call.message.bot.delete_message(chat_id=user_id, message_id=msg)
        except Exception as e:
            print(f"Error deleting message: {e}")
    
    
    if classes == 'boshqa':
        message_id = await send_bot_message(call.message.bot,user_id,'class1')
        await state.set_state(UserStates.classes2)
    else:
        message_id = await send_bot_message(call.message.bot,user_id,'school')
        await state.set_state(UserStates.school)
    await state.update_data(classes=classes,class1_id = message_id)
    await call.message.delete()

@user_private_router.message(F.text,UserStates.classes2)
async def classes(message:Message,state:FSMContext):
    data = await state.get_data()
    msg = data.get('class1_id')
    schools = message.text
    user_id = message.from_user.id
    if msg:
        try:
            await message.bot.delete_message(chat_id=user_id, message_id=msg)
        except Exception as e:
            print(f"Error deleting message: {e}")
    message_id = await send_bot_message(message.bot,user_id,'school')
    await state.update_data(classes=schools,class1_id = message_id)
    await state.set_state(UserStates.school)
    await message.delete()

@user_private_router.message(F.text,UserStates.school)
async def test(message:Message,state:FSMContext):
    data = await state.get_data()
    msg = data.get('class1_id')
    user_id = message.from_user.id
    school = message.text
    if msg:
        try:
            await message.bot.delete_message(chat_id=user_id, message_id=msg)
        except Exception as e:
            print(f"Error deleting message: {e}")
    message_id = await send_bot_message(message.bot,user_id,'teacher_name')
    await state.update_data(school=school,tch_id=message_id)
    await state.set_state(UserStates.teacher)
    await message.delete()

@user_private_router.message(F.text,UserStates.teacher)
async def test(message:Message,state:FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    msg = data.get('tch_id')
    if msg:
        try:
            await message.bot.delete_message(chat_id=user_id, message_id=msg)
        except Exception as e:
            print(f"Error deleting message: {e}")
    try:
        name_parts = message.text.split()

        if len(name_parts) != 2:
            raise ValueError("Expected two names")

        last_name, first_name = name_parts

        if not (last_name.endswith('v') or last_name.endswith('a')):
            raise ValueError("Invalid last name format")
        
        await state.update_data(teacher_name=first_name,teacher_last=last_name)
        await send_bot_message(message.bot,user_id,'contact')
        await state.set_state(UserStates.contact)
    except ValueError:
        await send_bot_message(message.bot,user_id,'wrong_fullname')
    await message.delete()

@user_private_router.message(F.contact,UserStates.contact)
async def con(message:Message,state:FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    schools = data.get('classes')
    school = data.get('school')
    tch_name = data.get('teacher_name')
    tch_last = data.get('teacher_last')
    contact = message.contact.phone_number

    bot_text = {
        'name': first_name,
        'last': last_name,
        'schools':schools,
        'school': school,
        'tch_name': tch_name,
        'tch_last': tch_last,
        'contact': contact
    }
    await state.update_data(contact=contact)
    await send_bot_message(message.bot,user_id,'correct_login',bot_text)
    await state.set_state(UserStates.yes)
    await message.delete()

@user_private_router.callback_query(F.data=='accept',UserStates.yes)
async def yes(call:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    user_id = call.from_user.id
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    male = data.get('male')
    schools = data.get('classes')
    school = data.get('school')
    tch_name = data.get('teacher_name')
    tch_last = data.get('teacher_last')
    contact = data.get('contact')
    await sync_to_async(UserCreate.objects.create)(
        telegram_id = user_id,
        first_name = first_name,
        last_name = last_name,
        schools = schools,
        school = school,
        teacher_name = tch_name,
        teacher_last = tch_last,
        number = contact,
        male = male
    )
    await send_bot_message(call.message.bot,user_id,'start')
    await state.clear()

@user_private_router.callback_query(F.data=='reject',UserStates.yes)
async def no(call:CallbackQuery,state:FSMContext):
    user_id = call.from_user.id
    await send_bot_message(call.message.bot,user_id,'full_name')
    message_id = await state.set_state(UserStates.full_name)
    await state.update_data(name_id=message_id)
    await call.message.delete()