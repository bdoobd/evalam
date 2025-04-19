export const formatDate = function (date_string) {
    const date_obj = new Date(Date.parse(date_string))
    const options = {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
    }
    const formater = new Intl.DateTimeFormat('fi-FI', options)

    return formater.format(date_obj)
}