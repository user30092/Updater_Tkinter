const mineflayer = require('mineflayer');
const fs = require('fs');
const path = require('path');
const mcData = require('minecraft-data');
const bot = mineflayer.createBot({
    host: 'localhost',
    port: 25565,
    username: 'RandomBot'
});



function findNearest(bot, max=10) {
    return Object.values(bot.entities)
        .filter(e => e.type === 'player' 
            && e.position.distanceTo(bot.entity.position) <= max 
            && e !== bot.entity)
        .sort((a,b) => a.position.distanceTo(bot.entity.position) - b.position.distanceTo(bot.entity.position))[0];
}

function smoothLookAt(bot, target, duration = 1000) {
    const startYaw = bot.entity.yaw;
    const startPitch = bot.entity.pitch;

    const targetYaw = Math.atan2(-target.x, -target.z);
    const targetPitch = Math.asin(target.y / target.xzDistanceTo(bot.entity.position));

    const yawDiff = targetYaw - startYaw;
    const pitchDiff = targetPitch - startPitch;

    const steps = 20; // Количество шагов для плавного поворота
    const yawStep = yawDiff / steps;
    const pitchStep = pitchDiff / steps;

    let currentStep = 0;

    const interval = setInterval(() => {
        if (currentStep >= steps) {
            clearInterval(interval);
            return;
        }

        bot.look(startYaw + yawStep * currentStep, startPitch + pitchStep * currentStep, true);
        currentStep++;
    }, duration / steps);
}

function lookAtNearestEntity(bot) {
    const nearestEntity = findNearest(bot);

    if (nearestEntity) {
        // Вычисляем точные координаты для поворота
        const target = nearestEntity.position.offset(0, nearestEntity.height, 0);
        const delta = target.minus(bot.entity.position);

        // Вычисляем углы поворота
       smoothLookAt(bot, delta);

        // Плавный поворот головы
		bot.attack(nearestEntity);

        console.log(`Поворот к ${nearestEntity.username || nearestEntity.type}`);
    }
}


// Дополнительные обработчики для логирования сущностей
bot.on('entitySpawn', (entity) => {
    if (entity.type === 'player' || entity.type === 'animal') {
        console.log(`Появилась сущность: ${entity.username || entity.type}`);
    }
});

bot.on('entityGone', (entity) => {
    if (entity.type === 'player' || entity.type === 'animal') {
        console.log(`Исчезла сущность: ${entity.username || entity.type}`);
    }
});


function processMovement(actionData) {
    // Сброс всех состояний перед новыми действиями
    bot.clearControlStates();
	

    // Более плавное движение
    const moveActions = {
        'forward': () => bot.setControlState('forward', true),
        'back': () => bot.setControlState('back', true),
        'left': () => bot.setControlState('left', true),
        'right': () => bot.setControlState('right', true),
        'stop': () => {} // Явно ничего не делаем
    };

    // Безопасный вызов движения
    const moveAction = moveActions[actionData.move];
    if (moveAction) moveAction();

    // Более точный поворот
    const lookActions = {
        'up': () => bot.look(bot.entity.yaw, bot.entity.pitch - 0.5),
        'down': () => bot.look(bot.entity.yaw, bot.entity.pitch + 0.5),
        'left': () => bot.look(bot.entity.yaw - 0.5, bot.entity.pitch),
        'right': () => bot.look(bot.entity.yaw + 0.5, bot.entity.pitch)
    };

    const lookAction = lookActions[actionData.look];
    if (lookAction) lookAction();
}


function processAction() {
    try {
        const actionPath = path.join(__dirname, 'action.json');
        const actionData = JSON.parse(fs.readFileSync(actionPath, 'utf8'));
        
        // Движение и поворот
        processMovement(actionData);
		lookAtNearestEntity(bot);
		
		bot.setQuickBarSlot(actionData.container); // Выбирает первый слот

        // Прыжок и спринт с дополнительными проверками
        bot.setControlState('jump', actionData.jump === 'true');
        bot.setControlState('sprint', actionData.sprint === 'true');

    } catch (error) {
        console.error('Ошибка при чтении действия:', error);
    }
}

bot.on('spawn', () => {
    console.log('Бот появился в мире');
    
    setTimeout(() => {
        setInterval(processAction, 500);
    }, 1000);
});

bot.on('chat', (username, message) => {
  if (username === bot.username) return;
  if (message.includes('/login')) {
    bot.chat('/login пароль'); // Замени "пароль" на свой
  } else if (message.includes('/register')) {
    bot.chat('/register пароль пароль'); // Замени "пароль" на свой
  }
});
