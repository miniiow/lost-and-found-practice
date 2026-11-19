# 분실물 관리 서비스 - 코드 품질 실습용 
import os, sys
import datetime

items = []
NEXT_NO = 1

def RegisterItem(name,category,found_date,location,finder,memo):
    global NEXT_NO
    if name == None or name == "":
        return "물품명을 입력하세요"
    if category == None or category == "":
        return "분류를 입력하세요"
    l = len(name)
    item = {"no": "P" + str(NEXT_NO), "name": name, "category": category, "found_date": found_date, "location": location, "status": "보관 중"}
    items.append(item)
    NEXT_NO+=1
    return item["no"]

def _format_item(item):
    """검색 결과 한 줄을 만든다."""
    return (item["no"] + " " + item["name"]
            + " [" + item["category"] + "]"
            + " 습득일 " + item["found_date"]
            + " / 보관 장소 " + item["location"])


def _search_stored_items(field, keyword):
    """보관 중인 물품 중 field 값에 keyword가 포함된 물품을 찾아 결과 문자열 목록으로 반환한다."""
    result = []
    for item in items:
        if item["status"] == "보관 중" and keyword in item[field]:
            result.append(_format_item(item))
    if len(result) == 0:
        print("검색 결과가 없습니다. 학생지원팀에 문의하세요.")
    return result


def search_by_name(keyword):
    return _search_stored_items("name", keyword)


def search_by_category(keyword):
    return _search_stored_items("category", keyword)

def _is_blank(value):
    """None 또는 빈 문자열이면 True."""
    return value == None or value == ""


def _find_item(item_no):
    """물품 번호로 물품을 찾는다. 없으면 None."""
    for item in items:
        if item["no"] == item_no:
            return item
    return None


def _check_status(item):
    """인도 가능한 상태인지 확인한다. 문제가 있으면 오류 메시지, 없으면 None."""
    if item["status"] == "인도 완료":
        return "이미 인도된 물품입니다"
    if item["status"] != "보관 중":
        return "알 수 없는 상태입니다"
    return None


def _check_handover_input(owner_checked, today, staff):
    """인도 입력값을 검증한다. 문제가 있으면 오류 메시지, 없으면 None."""
    if owner_checked != True:
        return "주인 확인이 필요합니다"
    if _is_blank(today):
        return "인도일을 입력하세요"
    if _is_blank(staff):
        return "담당자를 입력하세요"
    return None


def _complete_handover(item, today, staff):
    """물품을 인도 완료 상태로 변경한다."""
    item["status"] = "인도 완료"
    item["handover_date"] = today
    item["staff"] = staff


def handover(item_no, owner_checked, today, staff):
    if _is_blank(item_no):
        return "물품 번호를 입력하세요"

    item = _find_item(item_no)
    if item is None:
        return "등록되지 않은 물품 번호입니다"

    error = _check_status(item)
    if error is None:
        error = _check_handover_input(owner_checked, today, staff)
    if error is not None:
        return error

    _complete_handover(item, today, staff)
    return "인도 완료"

def count_by_status():
    try:
        stored = len([i for i in items if i["status"] == "보관 중"])
        handed = len([i for i in items if i["status"] == "인도 완료"])
    except:
        return None
    return {"보관 중": stored, "인도 완료": handed}

if __name__ == "__main__":
    RegisterItem("검정 우산", "기타", "2026-11-12", "학생지원팀 보관함", "학생A", "")
    print(search_by_name("우산")); print(handover("P1", True, "2026-11-19", "담당자A"))
    print(count_by_status())
