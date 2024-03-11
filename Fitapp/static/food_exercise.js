const { createApp } = Vue;

// @cardType: 'food' or 'exercise
function loadCards(cardType, page = 1, pageSize = 12, searchBy = '') {
    let apiUrl = (cardType === 'food') ? '/nutrition/food_list/' : '/fitness/exercise_list/';
    if (searchBy !== '') {
        apiUrl += '?search=' + encodeURIComponent(searchBy);
    }

    return fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            return data.map(item => ({
                id: item.id,
                image: item.image,
                name: item.name,
                category: item.category,
                calorie: Math.round(item.calorie)
            }));
        })
        .catch(error => {
            console.error('Fetch error:', error);
            return [];
        });
}


// @recordType: 'food' or 'exercise
// @entity: id of the food or exercise
function saveRecord(recordType, entityId, quantity) {
    let today = new Date()
    return 'ok'
    // TODO backend API
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
                this.cards = loadCards(this.pageType, 1, 12, this.searchInput)
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