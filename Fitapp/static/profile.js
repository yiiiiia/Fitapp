const { createApp } = Vue;

function isInteger(string) {
    return /^[1-9][0-9]*$/.test(string);
}

const app = createApp({
    mounted() {
        if (profileComplete == 'True') {
            this.form.gender = initGender
            this.form.age = parseInt(initAge)
            this.form.height = parseFloat(initHeight)
            this.form.weight = parseFloat(initWeight)
        } else {
            this.edit()
        }
    },
    data() {
        return {
            form: {},
            err: {},
        }
    },
    methods: {
        edit() {
            this.$refs['profile-form'].classList.remove('is-hidden')
            this.$refs['profile-table'].classList.add('is-hidden')
        },
        closeEdit() {
            let gender = this.form.gender
            gender = gender.charAt(0).toUpperCase() + gender.slice(1)
            this.$refs.gender.innerHTML = gender
            this.$refs.age.innerHTML = this.form.age

            let height = parseFloat(this.form.height).toFixed(1)
            this.$refs.height.innerHTML = height
            let weight = parseFloat(this.form.weight).toFixed(1)
            this.$refs.weight.innerHTML = weight
            this.$refs['profile-form'].classList.add('is-hidden')
            this.$refs['profile-table'].classList.remove('is-hidden')
        },
        closeNotice() {
            if (this.$refs.notice) {
                this.$refs.notice.classList.add('is-hidden')
            }
        },
        validate() {
            let valid = true
            if (this.form.age <= 0 || this.form.age > 150) {
                valid = false
                this.err.age = 'not a valid age'
            }
            if (this.form.height <= 0 || this.form.height > 300) {
                valid = false
                this.err.height = 'not a valid height'
            }
            if (this.form.weight <= 0 || this.form.weight > 300) {
                valid = false
                this.err.height = 'not a valid weight'
            }
            return valid
        },
        submit() {
            if (this.validate()) {
                console.log(this.form)
                const csrftoken = Cookies.get('csrftoken')
                fetch('/userprofile/profile/', {
                    method: 'post',
                    mode: 'same-origin',
                    headers: {
                        "Content-Type": "application/json",
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({
                        'gender': this.form.gender,
                        'age': parseInt(this.form.age),
                        'height': parseFloat(this.form.height),
                        'weight': parseFloat(this.form.weight)
                    })
                }).then(resp => {
                    if (resp.status == 200) {
                        let message = 'Profile updated!'
                        if (profileComplete == 'True') {
                            message = 'Profile created!'
                        }
                        Swal.fire({
                            title: 'Success!',
                            text: message,
                            icon: 'success',
                            confirmButtonText: 'OK'
                        }).then(() => {
                            if (profileComplete == 'True') {
                                this.closeEdit()
                            } else {
                                window.location.href = '/fitness/dashboard/'
                            }
                        });
                    }
                }).catch(err => {
                    console.log(err)
                })
            }
        }
    },
    compilerOptions: {
        delimiters: ["[[", "]]"]
    }
}).mount('#app-profile')