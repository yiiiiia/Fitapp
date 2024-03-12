const { createApp } = Vue;
const validateEmail = (email) => {
    return String(email)
        .toLowerCase()
        .match(
            /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        );
};

class Input {
    style = 'input';
    check = 0;
    msg = '';

    reset() {
        this.style = 'input';
        this.check = 0;
        this.msg = '';
    }

    ok(okMsg) {
        this.style = 'input is-primary'
        this.check = 1;
        this.msg = okMsg
    }

    error(errMsg) {
        this.style = 'input is-danger'
        this.check = 2
        this.msg = errMsg
    }

    get unchecked() {
        return this.check == 0
    }

    get checkOk() {
        return this.check == 1
    }

    get checkErr() {
        return this.check == 2
    }
}

const app = createApp({
    data() {
        return {
            form: {},
            username: new Input(),
            email: new Input(),
            password: new Input(),
            password2: new Input(),
        };
    },
    methods: {
        async submit() {
            if (this.username.checkOk && this.email.checkOk && this.password.checkOk && this.password2.checkOk) {
                if (!this.form.agree) {
                    this.form.needConfirm = true
                    return
                }
                const csrftoken = Cookies.get('csrftoken');
                this.form.needConfirm = false
                const resp = await fetch(this.$refs.form.action, {
                    method: 'post',
                    mode: 'same-origin',
                    headers: {
                        "Content-Type": "application/json",
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({ 'username': this.form.username, 'password': this.form.password, 'email': this.form.email })
                })
                if (resp.status == 201) {
                    window.location.href = '/userprofile/profile/'
                } else {
                    alert('server internal error')
                }
            }
        },
        check_username() {
            const username = this.form.username
            if (username) {
                fetch('/userprofile/signup_check?username=' + encodeURIComponent(username)).then((resp) => {
                    resp.json().then((val) => {
                        if (val.exists) {
                            this.username.error('This username already exists')
                        } else {
                            this.username.ok('')
                        }
                    })
                })
            }
        },
        change_username() {
            this.username.reset()
        },
        check_email() {
            const email = this.form.email
            if (!email) {
                return
            }
            if (!validateEmail(email)) {
                this.email.error('Not valid Email')
                return
            }
            fetch('/userprofile/signup_check?email=' + encodeURIComponent(email)).then((resp) => {
                resp.json().then((val) => {
                    if (val.exists) {
                        this.email.error('This email is registered')
                    } else {
                        this.email.ok('')
                    }
                })
            })
        },
        change_email() {
            this.email.reset()
        },
        check_password() {
            this.check_pass_confirm()
            const pass = this.form.password
            if (!pass) {
                return
            }
            if (pass.length < 8) {
                this.password.error('Password should be at least 8 characters')
                return
            }
            if (pass.indexOf(' ') > 0) {
                this.password.error('Password should not contain space character')
                return
            }
            count = 0
            const specialChars = '!@#$%^&*()_'
            for (ch of pass) {
                if (specialChars.indexOf(ch) >= 0) {
                    count++;
                }
            }
            if (count < 2) {
                this.password.error('Password should contain at least 2 special characters')
                return
            }
            this.password.ok('')
        },
        change_password() {
            this.password.reset()
        },
        check_pass_confirm() {
            if (!this.form.password_confirm) {
                return
            }
            if (this.form.password != this.form.password_confirm) {
                this.password2.error('Passwords do not match')
                return
            }
            if (this.password.checkOk) {
                this.password2.ok('')
            } else {
                this.password2.reset('')
            }
        }
    },
    compilerOptions: {
        delimiters: ["[[", "]]"]
    }
}).mount('#app-signup')