import { formatDate } from '../helpers.js'

class Home {
    _parentElement = document.querySelector('main')

    render(data = {}) {

        // this.getOnStokcckData();

        let table = this._tableMarkup(data)
        this._parentElement.insertAdjacentHTML('afterbegin', table)
    }

    addHandlerHome(handler) {
        handler();
    }

    async getOnStockData() {
        const url = '/item/items';
        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail)
            }

            const result = await response.json();

            return this._tableRow(result)
            
        } catch (e) {
            console.log(e);
        }
    }

    _tableMarkup(data = {}) {
        return `
            <h1 class="d-flex">Items on stock</h1>
            <div id="modalDialogWindow"></div>
                <table class="table table-striped caption-top">
                    <thead>
                        <tr>
                            <th scope="col">Stock</th>
                            <th scope="col">Date</th>
                            <th scope="col">Type</th>
                            <th scope="col">Name</th>
                            <th scope="col">Width</th>
                            <th scope="col">Pallet</th>
                            <th scope="col">Lot</th>
                            <th scope="col">Roll</th>
                            <th scope="col" class="col-width-5">&nbsp;</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${this.getOnStockData()}
                    </tbody>
                    </table>
        `;
    }

    _tableRow(jsonData) {
        console.log(jsonData);

        for (const [key, value] of Object.entries(jsonData)) {
           console.log(`Key ${key}, value ${value}`);
       }

        
        
        // {% for item in items %}
        // <tr>
        // <th scope="row">{{ item.stock.reference }}</th>
        // <td>{{ item.stock.date }}</td>
        // <td>{{ item.cat.cat }}</td>
        // <td>{{ item.cat.name }}</td>
        // <td>{{ item.cat.width }}</td>
        // <td>{{ item.pallet }}</td>
        // <td>{{ item.lot }}</td>
        // <td>{{ item.roll }}</td>
        // <td>
        //     <img
        //     src="./static/images/edit.svg"
        //     alt="Edit item"
        //     />
        // </td>
        // </tr>
        // {% endfor %}
    }
}

export default new Home();