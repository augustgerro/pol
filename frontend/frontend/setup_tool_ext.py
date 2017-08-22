from hashlib import md5

from scrapy.selector import Selector

from .settings import SNAPSHOT_DIR


def build_xpath_results(selectors, file_name):
    feed_xpath = selectors[0]
    field_xpathes = selectors[1]

    fpath = "%s/%s" % (SNAPSHOT_DIR, file_name)

    with open(fpath) as f:
        data = f.read()

    html = data.decode('utf-8').split('\n\n', 1)[1]

    feed_result = None
    field_results = {}

    extracted_posts = []

    success = True
    post_elems = None
    try:
        doc = Selector(text=html)
        post_elems = doc.xpath(feed_xpath)
        feed_result = {'count': len(post_elems)}

        if post_elems:
            for elem in post_elems:
                selected_required = True
                selected_link = True
                extracted_post = {}
                for name, xpath in field_xpathes.iteritems():
                    if not (name in field_results):
                        field_results[name] = {}
                    xpath = xpath.strip()
                    try:
                        extracts = elem.xpath(xpath).extract()
                        if name == 'link':
                            if not extracts:
                                selected_link = False
                            else:
                                extracted_post[name] = u''.join(extracts)
                        else:
                            if not extracts:
                                selected_required = False
                            else:
                                extracted_post[name] = u''.join(extracts)
                    except ValueError as ex:
                        success = False
                        field_results[name]['error'] = ex.message

                if selected_required:
                    for name, xpath in field_xpathes.iteritems():
                        if name == 'link':
                            if selected_link:
                                if 'count' in field_results[name]:
                                    field_results[name]['count'] += 1
                                else:
                                    field_results[name]['count'] = 1
                        else:
                            if 'count' in field_results[name]:
                                field_results[name]['count'] += 1
                            else:
                                field_results[name]['count'] = 1

                    extracted_posts.append(extracted_post)
            else:
                for name, xpath in field_xpathes.iteritems():
                    xpath = xpath.strip()
                    try:
                        doc.xpath(xpath).extract()
                    except ValueError as ex:
                        if not (name in field_results):
                            field_results[name] = {}
                        field_results[name]['error'] = ex.message
                        success = False


    except ValueError as ex:
        feed_result = {'error': ex.message}
        success = False

    return [[feed_result, field_results], extracted_posts, success]
