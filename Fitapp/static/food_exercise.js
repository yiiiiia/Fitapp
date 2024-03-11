const { createApp } = Vue;

// @cardType: 'food' or 'exercise
async function loadCards(cardType, page = 1, pageSize = 12, searchBy = '') {
    let apiUrl = (cardType === 'food') ? '/nutrition/food_list/' : '/fitness/exercise_list/';
    if (searchBy !== '') {
        apiUrl += '?search=' + encodeURIComponent(searchBy);
    }

    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data.map(item => ({
            id: item.id,
            image: item.image,
            name: item.name,
            category: item.category,
            calorie: Math.round(item.calorie)
        }));
    } catch (error) {
        console.error('Fetch error:', error);
        return [];
    }
}


// @recordType: 'food' or 'exercise
// @entity: id of the food or exercise
async function saveRecord(recordType, entityId, quantity) {
    let apiUrl = (recordType === 'food') ? '/nutrition/add_food_eaten/' : '/fitness/add_exercise_done/';
    let payload = {
        food: entityId,
        amount: quantity,
        date: new Date().toISOString().split('T')[0]
    };

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
        return data.message;
    } catch (error) {
        console.error('Save record error:', error);
        return 'Error';
    }
}

const foodExerciseApp = createApp({
    mounted() {
        let pageType = this.$refs.root.getAttribute('page_type')
        this.pageType = pageType
        if (pageType == 'food') {
            this.quantityPlaceholder = 'unit: g'
            this.searchPlaceholder = 'Search food'
        } else if (pageType == 'exercise') {
            this.quantityPlaceholder = 'unit: minute'
            this.searchPlaceholder = 'Search exercise'
        }
        this.loadCards()
    },
    data() {
        return {
            pageType: '',
            cards: [],
            exerciseCards: [],
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
            if (this.searchInput != '') {
                loadCards(this.pageType, 1, 12, this.searchInput).then(cards => {
                    this.cards = cards;
                });
            }
        },
        loadCards() {
            loadCards(this.pageType).then(cards => {
                this.cards = cards;
            });
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
        submit() {
            if (this.saveQuantity == '') {
                this.$refs.num_input.classList.add('is-danger')
                this.inputErr = (this.pageType == 'food' ? 'Quantity' : 'Time') + ' is required'
                return
            }
            if (isNaN(this.saveQuantity)) {
                this.$refs.num_input.classList.add('is-danger')
                this.inputErr = 'not a number'
                return
            }
            if (saveRecord(this.pageType, this.recordItem.id, parseInt(this.saveQuantity, 10))) {
                this.deactivateModal()
            } else {
                alert('Network error')
            }
        }
    },
    compilerOptions: {
        delimiters: ["${", "}$"]
    }
}).mount('#food_exercise_app')