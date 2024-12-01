$(function () {
    // Load initial shareholder data
    let shareholdersInput = $('#shareholdersInput').val();
    let shareholders = [];

    if (shareholdersInput) {
        try {
            shareholders = JSON.parse(shareholdersInput);
        } catch (error) {
            console.error("Invalid JSON:", error);
        }
    }

    let selectedShareholder = {};

    const shareholdersContainer = $('#shareholders');
    const shareholderTemplate = shareholdersContainer.html();

    shareholdersContainer.find('li:first').remove();

    showShareholderRows(shareholders);
    disableShareholderForm(true);

    $('#addShareholder').click(function () {
        addShareholder();
    });

    $('#submitForm').click(function () {
        $('#shareholdersInput').val(JSON.stringify(shareholders, null, 2));
        $('#companyForm').submit();
    });

    function countShareholders() {
        return shareholders.length;
    }

    function addShareholder() {
        if (!shareholders.some(shareholder => shareholder.id === selectedShareholder.id && shareholder.type === selectedShareholder.type)) {
            shareholders.push(selectedShareholder);
        }

        console.log("Shareholders: ", shareholders);

        resetShareholderForm();
        showShareholderRows(shareholders);
    }

    function resetShareholderForm() {
        selectedShareholder = {};
        $('#shareholderSearchInput').val('');
        disableShareholderForm(true);
    }

    function disableShareholderForm(isDisabled) {
        $('#addShareholder').prop('disabled', isDisabled);
    }

    function showShareholderRows(shareholders) {
        removeShareholderRows();

        shareholders.forEach(function (shareholder) {
            showShareholderRow(shareholder.id, shareholder.type, shareholder.name, shareholder.code, shareholder.share_amount);
        });
    }

    function updateShareholderShareAmount(id, type, shareAmount) {
        let shareholder = shareholders.find(shareholder => shareholder.id == id && shareholder.type == type);
        shareholder.share_amount = parseInt(shareAmount);
    }

    function deleteShareholder(id, type) {
        console.log(`Deleting shareholder (${id}, ${type})`);
        shareholders = shareholders.filter(shareholder => !(shareholder.id == id && shareholder.type == type));

        showShareholderRows(shareholders);
    }

    function showShareholderRow(id, type, name, code, shareAmount) {
        const shareholderRow = $(shareholderTemplate);
        const row = countShareholders() - 1;

        shareholderRow.find('[data-shareholder-name]').text(name);
        shareholderRow.find('[data-shareholder-type]').text(type);
        shareholderRow.find('[data-shareholder-code]').text(code);
        shareholderRow.find('[data-shareholder-share-amount]').text(shareAmount);

        shareholderRow.find('input[data-shareholder-type]').attr('name', `shareholders[${row}][type]`).val(type);
        shareholderRow.find('input[data-shareholder-id]').attr('name', `shareholders[${row}][id]`).val(id);
        shareholderRow.find('input[data-shareholder-share-amount]').attr('name', `shareholders[${row}][share_amount]`).val(shareAmount);

        shareholderRow.find('input[data-shareholder-share-amount]').on('input', function () {
            const updatedShareAmount = $(this).val();

            const parentContainer = $(this).closest('li');
            const shareholderId = parentContainer.find('input[data-shareholder-id]').val();
            const shareholderType = parentContainer.find('input[data-shareholder-type]').val();

            updateShareholderShareAmount(shareholderId, shareholderType, updatedShareAmount);
            console.log(`Updated share amount (${id}): ${updatedShareAmount}`);
        });

        shareholderRow.find('button[data-shareholder-remove]').click(function () {
            if (!confirm('Are you sure you want to remove this shareholder?')) {
                return;
            }

            const parentContainer = $(this).closest('li');
            const shareholderId = parentContainer.find('input[data-shareholder-id]').val();
            const shareholderType = parentContainer.find('input[data-shareholder-type]').val();

            deleteShareholder(shareholderId, shareholderType);
            console.log(`Delete shareholder (${id})`);
        });

        shareholdersContainer.append(shareholderRow);
    }

    function removeShareholderRows() {
        shareholdersContainer.find('li').remove();
    }

    $("#shareholderSearchInput").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: SHAREHOLDERS_SEARCH_URL,
                dataType: "json",
                data: {
                    search: request.term
                },
                success: function (data) {
                    const formattedData = data.shareholders.map(function (item) {
                        if (item.type == 'company') {
                            return {
                                label: `${item.name} (${item.code})`,
                                value: item.name,
                                id: item.id,
                                name: item.name,
                                type: 'Company',
                                code: item.code,
                            };
                        } else {
                            return {
                                label: `${item.first_name} ${item.last_name} (${item.code})`,
                                value: item.first_name + ' ' + item.last_name,
                                id: item.id,
                                first_name: item.first_name,
                                last_name: item.last_name,
                                type: 'Person',
                                code: item.code,
                            };
                        }
                    });
                    response(formattedData);
                }
            });
        },
        minLength: 2,
        select: function (event, ui) {
            // Handle selection
            console.log("Selected:", ui.item);

            selectedShareholder = {
                'id': ui.item.id,
                'type': ui.item.type,
                'name': ui.item.value,
                'code': ui.item.code,
                'share_amount': null,  // Default share amount
            };

            disableShareholderForm(false);
        }
    });

});
