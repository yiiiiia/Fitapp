const { createApp } = Vue;

// @recordType: 'food' or 'exercise
// @entity: id of the food or exercise
async function saveRecord(recordType, entityId, quantity) {
    let apiUrl = (recordType === 'food') ? '/nutrition/add_food_eaten/' : '/fitness/add_exercise_done/';
    let payload;
    if (recordType === 'food') {
        payload = {
            food: entityId,
            amount: quantity,
            date: new Date().toISOString().split('T')[0]
        };
    } else if (recordType === 'exercise') {
        payload = {
            exercise: entityId,
            duration: quantity,
            date: new Date().toISOString().split('T')[0]
        };
    }

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': Cookies.get('csrftoken')
            },
            body: JSON.stringify(payload),
            credentials: 'include'
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return {
            message: data.message,
            calories: data.calories,
            type: recordType
        };
    } catch (error) {
        console.error('Save record error:', error);
        return { message: 'Error', calories: 0, type: recordType };
    }
}

const foodExerciseApp = createApp({
    mounted() {
        this.pageType = pageType
        if (this.pageType == 'food') {
            this.quantityPlaceholder = 'unit: g'
            this.searchPlaceholder = 'Search food'
        } else if (this.pageType == 'exercise') {
            this.quantityPlaceholder = 'unit: minute'
            this.searchPlaceholder = 'Search exercise'
        }
        this.loadCards('')
    },
    data() {
        return {
            pageType: '',
            cards: [],
            recordItem: {},
            inputErr: '',
            quantityPlaceholder: '',
            searchPlaceholder: '',
            saveQuantity: '',
            searchInput: '',
        }
    },
    methods: {
		searchByName() {
			this.loadCards(this.searchInput)
		},
        async loadCards(searchBy) {
            let apiUrl = (this.pageType === 'food') ? '/nutrition/food_list/' : '/fitness/exercise_list/';
            if (searchBy !== '') {
                apiUrl += '?search=' + encodeURIComponent(searchBy);
            }

            try {
                const response = await fetch(apiUrl);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                if (this.pageType === 'food') {
                    this.cards = data.map(item => ({
                        id: item.id,
                        image: item.image,
                        category: item.food_type,
                        name: item.food_name,
                        calorie: Math.round(item.calories_per_gram)
                    }));
                } else if (this.pageType == 'exercise') {
                    this.cards = data.map(item => ({
                        id: item.id,
                        image: item.image,
                        name: item.exercise_name,
                        calorie: Math.round(item.calories_per_min)
                    }));
                }
            } catch (error) {
                console.error('Fetch error:', error);
            }
        },
        activateModal(item) {
            this.recordItem = item
            this.saveQuantity = ''
            this.$refs.modal.classList.add('is-active')
        },
        deactivateModal() {
            this.$refs.modal.classList.remove('is-active')
        },
        clearErr() {
            this.$refs.num_input.classList.remove('is-danger')
            this.inputErr = ''
        },
        async submit() {
            if (this.saveQuantity == '') {
                this.$refs.num_input.classList.add('is-danger');
                this.inputErr = (this.pageType == 'food' ? 'Quantity' : 'Time') + ' is required';
                return;
            }
            if (isNaN(this.saveQuantity)) {
                this.$refs.num_input.classList.add('is-danger');
                this.inputErr = 'not a number';
                return;
            }
            const result = await saveRecord(this.pageType, this.recordItem.id, parseInt(this.saveQuantity, 10));
            if (result.message !== 'Error') {
                let message = '';
                if (result.type === 'food') {
                    message = `Calories Added: ${result.calories}`;
                } else {
                    message = `Calories Burned: ${result.calories}`;
                }
                Swal.fire({  // use SweetAlert2 box
                    title: 'Success!',
                    text: message,
                    icon: 'success',
                    confirmButtonText: 'OK'
                }).then(() => {
                    this.deactivateModal();  // 关闭模态框
                });
            } else {
                Swal.fire({
                    title: 'Error',
                    text: 'There was a problem saving the record.',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        }
    },
    compilerOptions: {
        delimiters: ["${", "}$"]
    }
}).mount('#food_exercise_app')
