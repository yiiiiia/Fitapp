const { createApp } = Vue;
const app = createApp({
    data() {
        return {
            form: {},
            inputClass: 'input',
            errcode: 0
        };
    },
    methods: {
        setNormal() {
            this.inputClass = 'input'
            this.errcode = 0
        },
        async submit() {
            try {
                const csrftoken = Cookies.get('csrftoken')
                const resp = await fetch('/userprofile/login/', {
                    method: 'post',
                    mode: 'same-origin',
                    headers: {
                        "Content-Type": "application/json",
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({ 'username': this.form.username, 'password': this.form.password })
                })
                if (resp.status == 200) {
                    this.setNormal()
                    resp.json().then((value) => {
                        window.location.href = value.next_page
                    })
                } else if (resp.status == 404) {
                    resp.json().then((value) => {
                        this.inputClass = 'input is-danger'
                        if (value.error == 'user not exist') {
                            this.errcode = 1
                        } else if (value.error == 'incorrect password') {
                            this.errcode = 2
                        }
                    })
                }
            } catch (e) {
                console.error(e)
            }
        },
    },
    compilerOptions: {
        delimiters: ["${", "}$"]
    }
}).mount('#login_app')