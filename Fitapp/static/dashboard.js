function parseDate(date) {
    let year = date.getFullYear()
    let month = date.getMonth()
    let day = date.getDate()
    if (month >= 0 && month < 10) {
        month = '0' + (month + 1)
    }
    if (day >= 1 && day < 10) {
        day = '0' + day
    }
    return year + '-' + month + '-' + day
}

function weekDayName(day) {
    if (day == 7) {
        return "Sun"
    }
    if (day == 1) {
        return "Mon"
    }
    if (day == 2) {
        return "Tue"
    }
    if (day == 3) {
        return "Wed"
    }
    if (day == 4) {
        return "Thu"
    }
    if (day == 5) {
        return "Fri"
    }
    if (day == 6) {
        return "Sat"
    }
    return ""
}

function getDaysOfThisWeek() {
    const today = new Date()
    let date = today.getDate()
    let weekDay = today.getDay()
    if (weekDay == 0) {
        weekDay = 7
    }
    let result = []
    for (let i = weekDay; i >= 1; --i) {
        today.setDate(date - i)
        result.push(parseDate(today))
    }
    return result
}

function getCalorieDeficitByDate(date) {
    // TODO backend API
    let randInt = function () {
        return Math.floor(Math.random() * 250)
    }

    let n = randInt()
    if (Math.random() <= 0.55) {
        return n;
    } else {
        return -n
    }
}

function getTodayIntake(date) {
    return fetch('/nutrition/food_daily/')
        .then(response => response.json());
}

const { createApp } = Vue;

const metabolismApp = Vue.createApp({
    data() {
        return {
            metabolismData: {
                exerciseMetabolism: 0,
                dailyBasalMetabolism: 0,
                caloriesTaken: 0,
                sumForToday: 0
            }
        };
    },
    mounted() {
        fetch('/nutrition/metabolism/')
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    const latestData = data[0];
                    this.metabolismData = latestData;
                }
                console.log('Today metabolism:', this.metabolismData);
            })
            .catch(error => console.error('Error:', error));
    }
}).mount('#metabolism-section');

const barApp = createApp({
    mounted() {
        this.loadMetabolismDataThisWeek();
    },
    data() {
        return {
            weeklyMetabolismData: []
        };
    },
    methods: {
        barStyle(n) {
            return `height: ${Math.abs(n)}px; background-color: #e6632c`;
        },
        loadMetabolismDataThisWeek() {
            fetch('/nutrition/metabolism_7days/')
                .then(response => response.json())
                .then(data => {
                    console.log('Received data from API:', data);
        
                    this.weeklyMetabolismData = data.map((item, index) => {
                        const dayName = weekDayName(new Date(item.date).getDay());
                        const total = item.total;
                        return { day: dayName, total: total };
                    });
        
                    console.log('Processed weekly metabolism data:', this.weeklyMetabolismData);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
        
    },
    compilerOptions: {
        delimiters: ["${", "}$"]
    }
}).mount('#calorie-bar');


const pieApp = createApp({
    mounted() {
        this.loadTodayIntake()
    },
    data() {
        return {
            today: new Date().toDateString(),
            intake: {
                fat: 0, carbohydrate: 0, protein: 0, other: 0
            }
        }
    },
    methods: {
        loadTodayIntake() {
            getTodayIntake().then(data => {
                this.intake = data;
                console.log('Today Intake:', this.intake);
            });
        },
        pieStyle() {
            return `background:
            conic-gradient(from 0deg,
                    #f7f25e 0,
                    #f7f25e calc(${this.intake.fat}%),
                    #67f594 calc(${this.intake.fat}%),
                    #67f594 calc(${this.intake.fat + this.intake.carbohydrate}%),
                    #cf5351 calc(${this.intake.fat + this.intake.carbohydrate}%),
                    #cf5351 calc(${this.intake.fat + this.intake.carbohydrate + this.intake.protein}%),
                    #166778 calc(${this.intake.fat + this.intake.carbohydrate + this.intake.protein}%),
                    #166778 calc(100%)
            )`
        }
    },
    compilerOptions: {
        delimiters: ["${", "}$"]
    }
}).mount('#calorie-pie')

const articleApp = createApp({
    mounted() {
        this.loadFavouriteArticles()
    },
    data() {
        return {
            articles: []
        }
    },
    methods: {
        loadFavouriteArticles() {
            // TODO backend API
            this.articles = [{
                title: 'One Twin Was Hurt, the Other Was Not. Their Adult Mental Health Diverged',
                content: 'Take Dennis and Douglas. In high school, they were so alike that friends told them apart by the cars they drove, they told researchers in a study of twins in Virginia. Most of their childhood experiences were shared — except that Dennis endured an attempted molestation when he was 13.'
            }, {
                title: 'F.D.A. Delays Action on Closely Watched Alzheimer’s Drug',
                content: 'The Alabama Supreme Court ruled last month that frozen embryos are human beings and those who destroy them can be held liable for wrongful death. Three of the state’s limited pool of IVF providers immediately paused services, sending some families out of state to access treatment and prompting a widespread and urgent demand for lawmakers to provide a fast fix.'
            }]
            console.log('hi,articles')
        }
    },
    compilerOptions: {
        delimiters: ["${", "}$"]
    }
}).mount('#favourite-articles')