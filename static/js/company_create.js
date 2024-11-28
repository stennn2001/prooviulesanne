$(function () {
    const shareholders = $('#shareholders');
    const shareholderTemplate = shareholders.html();

    shareholders.find('li:first').remove();

    $('#addShareholder').click(function () {
        addShareholder('person', $('#shareholderCode').val(), $('#shareholderShareAmount').val());
    });

    $('#submitForm').click(function () {
        var formData = $('form').serializeArray();
        var jsonData = {};

        formData.forEach(function (item) {
            var keys = item.name.replace(/\[|\]/g, '.').split('.');
            keys.reduce(function (acc, key, index) {
                if (index === keys.length - 1) {
                    acc[key] = item.value;
                } else {
                    if (!acc[key]) {
                        acc[key] = {};
                    }
                }
                return acc[key];
            }, jsonData);
        });

        console.log(JSON.stringify(jsonData));
    });

    function countShareholders() {
        return shareholders.children().length;
    }

    function addShareholder(type, code, shareAmount) {
        //TODO: API call

        const response = {
            'id': 1,
            'type': 'person',
            'name': 'John Doe',
            'code': 123456789,
        };

        addShareholderRow(response.id, response.type, response.name, response.code, shareAmount);
    }

    function addShareholderRow(id, type, name, code, shareAmount) {
        const shareholder = $(shareholderTemplate);
        const row = countShareholders() - 1;

        shareholder.find('[data-shareholder-name]').text(name);
        shareholder.find('[data-shareholder-type]').text(type);
        shareholder.find('[data-shareholder-code]').text(code);
        shareholder.find('[data-shareholder-share-amount]').text(shareAmount);

        shareholder.find('input[data-shareholder-type]').attr('name', `shareholders[${row}][type]`).val(type);
        shareholder.find('input[data-shareholder-id]').attr('name', `shareholders[${row}][id]`).val(id);
        shareholder.find('input[data-shareholder-share-amount]').attr('name', `shareholders[${row}][share_amount]`).val(shareAmount);

        shareholders.append(shareholder);
        console.log(shareholder.html());
    }
});