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
    // TODO backend API
    return {
        fat: 3, carbohydrate: 57, protein: 35, other: 5
    }
}

const { createApp } = Vue;

const barApp = createApp({
    mounted() {
        this.loadCalorieDeficitThisWeek()
    },
    data() {
        return {
            weeklyCalorieDeficits: []
        }
    },
    methods: {
        barStyle(n) {
            if (n >= 0) {
                return `height: ${Math.abs(n)}px; background-color: #e6632c`
            } else {
                return `height: ${-n}px; background-color: #2eb51f`
            }
        },
        loadCalorieDeficitThisWeek() {
            let daysOfThisWeek = getDaysOfThisWeek()
            let index = 1;
            for (let day in daysOfThisWeek) {
                let deficit = getCalorieDeficitByDate(day)
                this.weeklyCalorieDeficits.push({ 'day': weekDayName(index++), 'deficit': deficit })
            }
        }
    },
    compilerOptions: {
        delimiters: ["${", "}$"]
    }
}).mount('#calorie-bar')

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
            today = parseDate(new Date())
            // TODO backend api
            this.intake = getTodayIntake()
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