function init() {
    var $tabs = jQuery('.tabs .tab');
    $tabs.first().addClass('active');

    $tabs.click(onTabClick);

    var $pages = jQuery('.content .page');
    $pages.first().addClass('active');
}

function onTabClick(e) {
    var $tab = jQuery(e.currentTarget);
    var name = jQuery.trim($tab.text());

    var $tabs = jQuery('.tabs .tab');
    $tabs.removeClass('active');
    $tab.addClass('active');

    var $pages = jQuery('.content .page');
    $pages.removeClass('active');
    $pages.filter('[name="' + name + '"]').addClass('active');
}

jQuery(document).ready(init);