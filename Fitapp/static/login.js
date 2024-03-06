const { createApp } = Vue;
const app = createApp({
    data() {
        return {
            form: {},
            inputClass: 'input',
            loginErr: false
        };
    },
    methods: {
        setNormal() {
            this.inputClass = 'input'
            this.loginErr = false
        },
        setError() {
            this.inputClass = 'input is-danger'
            this.loginErr = true
        },
        async submit() {
            try {
                const csrftoken = Cookies.get('csrftoken');
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
                    this.setError()
                } else {
                    alert('Server is unavailable')
                }
            } catch (e) {
                console.error(e)
            }
        },
    }
});
app.config.compilerOptions.delimiters = ["[[", "]]"];
app.mount("#app");