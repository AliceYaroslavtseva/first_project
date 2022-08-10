from typing import Type, Dict, List


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories) -> None:
        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self) -> str:
        MESSAGE = ('Тип тренировки: {0}; '
                'Длительность: {1:.3f} ч.; '
                'Дистанция: {2:.3f} км; '
                'Ср. скорость: {3:.3f} км/ч; '
                'Потрачено ккал: {4:.3f}.').format(self.training_type,
                                                   self.duration,
                                                   self.distance,
                                                   self.speed,
                                                   self.calories)
        return MESSAGE


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HOUR: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        show = InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
        return show


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_RUN_1: float = 18
    COEFF_CALORIE_RUN_2: float = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_RUN_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_RUN_2) * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_WLK_1: float = 0.035
    COEFF_CALORIE_WLK_2: float = 0.029
    DEGREE: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CALORIE_WLK_1 * self.weight
                + (self.get_mean_speed() ** self.DEGREE // self.height)
                * self.COEFF_CALORIE_WLK_2 * self.weight)
                * (self.duration * self.MIN_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""
    COEFF_CALORIE_SWM_1: float = 1.1
    COEFF_CALORIE_SWM_2: float = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_CALORIE_SWM_1)
                * self.COEFF_CALORIE_SWM_2 * self.weight)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {
        'RUN': Running,
        'SWM': Swimming,
        'WLK': SportsWalking}
    if workout_type not in training_type:
        raise ValueError(f'Такой тренировки не существует: {workout_type}.')
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
