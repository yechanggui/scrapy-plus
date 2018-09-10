# -*- coding: utf-8 -*-
# @Author: Vincent <yecg@ruyi.ai>

import logging
import json
import  requests
import scrapy
import lxml.html

def html2table4lxml(dom, xpath_row, parse_config_list):
    """ 通用的表格属性抽取，以便后期处理
        dom is parsed by lxml.html.fromstring
        example params
        xpath_row = ".//div[@class='price-mod']//dl"
        map_attr_xpath_cell = {

        }
    """

    items = []
    rows = dom.xpath(xpath_row)
    if not rows:
        return items

    for row in rows:
        item = {}
        items.append(item)

        for extract_config in parse_config_list:
            cells  = row.xpath(extract_config["xpath"])
            if not cells:
                logging.warning("missing cell"+ json.dumps(extract_config))
                continue

            cell = cells[0]
            if extract_config.get('extract_text'):
                value = [x.strip() for x in cell.xpath(".//text()") if x.strip()]
                if extract_config.get('extract_text') == 'string':
                    value = u"".join(value)
                elif extract_config.get('extract_text') == 'string_first':
                    if value:
                        value = value[0]
                    else:
                        value = ""
                elif extract_config.get('extract_text') == 'string_list':
                    pass
                else:
                    logging.error("unexpected config {} {}".format(attr, xpath_cell) )
                    exit(0)

                _safe_set(item, extract_config["prop"], value )
            else:
                _safe_set(item, extract_config["prop"], cell )


    return items

####################################
# 2017-01-21
def html2json4lxml(dom, parse_config_list, default_extract_config = {"skip_empty":False, "extract_attrs":["class", "href", "id"]} ):
    # dom is lxml
    #通用的列表属性抽取，以便后期处理
    ret = {}
    if isinstance(dom, scrapy.http.response.html.HtmlResponse):
        dom = lxml.html.fromstring(dom.body)
    for parse_config in parse_config_list:
        assert 'xpath' in parse_config
        assert 'prop' in parse_config

        extract_config = {}
        extract_config.update(default_extract_config)
        extract_config.update(parse_config)
        # print extract_config
        # exit(0)
        temp_nodes = dom.xpath(parse_config['xpath'])
        if not temp_nodes:
            continue

        items = []
        for temp_node in temp_nodes:
            item = {}
            if extract_config.get('extract_text'):
                string_list = [x.strip() for x in temp_node.xpath(".//text()") if x.strip()]
                if extract_config.get('extract_text') == 'string':
                    _safe_set(item, "__text__", u"".join(string_list))
                else:
                    _safe_set(item, "__text__", string_list)

            for attr in extract_config.get("extract_attrs",[]):
                _safe_set(item, attr, temp_node.get(attr))


            if extract_config.get('skip_empty') and not item:
                pass
            else:
                items.append(item)

        if parse_config.get("op") == 'first':
            val = items[0].values()
            if val:
                if val in [unicode]:
                    ret[parse_config['prop']] = val
                elif val in [list]:
                    ret[parse_config['prop']] = val[0]
        else:
            ret[parse_config['prop']] = items
    #logging.info( json.dumps(ret,ensure_ascii=False, indent=4) )
    return ret


def _safe_set(item,k,v):
    if not v:
        return
    item[k]=v






