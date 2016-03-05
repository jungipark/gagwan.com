/**
 * Created by Jun on 15. 9. 3..
 */



$('.evl-attendent').rating({
    'size': 'xs', disabled: false, showClear: false, showCaption: true,
    'starCaptions': {
        0.5: '평가 못하겠음',
        1: '출첵이란 없다',
        1.5: '개강날 출첵 한번',
        2: '개강, 종강날만 출첵',
        2.5: '개강, 종강 + 그리고 1번',
        3: '3주에 한번 출첵',
        3.5: '음..출첵 가끔 안함',
        4: '매일 출첵',
        4.5: '매일 + 출석을 중요하게 생각하심',
        5: '쉬는 시간마다 출첵',
    }
});


$('.evl-grade').rating({
    'size': 'xs', disabled: false, showClear: false, showCaption: true,
    'starCaptions': {
        0.5: '평가 못하겠음',
        1: '성적은 포기하고 들음',
        1.5: '교수님 사전에 A는 없는듯',
        2: '시험 잘보고 + 매일 앞자리에서 공부',
        2.5: '계산기보다 정확한 성적평가',
        3: '하는만큼만 딱 줌',
        3.5: '하는만큼 만 딱 줌 + 0.5정도.. 더 주심',
        4: '모든 성적에 +을 달아줌',
        4.5: '성적 잘받기 위한 필수 수업',
        5: '성적자판기',
    }
});

$('.evl-amount').rating({
    'size': 'xs', disabled: false, showClear: false, showCaption: true,
    'starCaptions': {
        0.5: '평가 못하겠음',
        1: '숨쉬기 운동 수준',
        1.5: '1.5점 정도 어려움',
        2: '시험기간에만 하면됨',
        2.5: '시험기간 + 과제 2번 있음',
        3: '대학생이라면 이정도 공부는 해야지',
        3.5: '과제할당량 4번 다 채우심',
        4: '매 수업마다 과제',
        4.5: '한학기에 이런 강의 3개 이상은 힘듬',
        5: '진작 이렇게 공부했으면 하버드감',
    }
});

$('.evl-learning').rating({
    'size': 'xs', disabled: false, showClear: false, showCaption: true,
    'starCaptions': {
        0.5: '수업을 안들어감',
        1: '어떻게하면 편하게 잘수 있는지 깨달음',
        1.5: '기억나는것은 교수님 얼굴뿐',
        2: '심심할때 한번씩 수업 들어봄',
        2.5: '강의 핵심개념정도는 이해',
        3: 'So-So',
        3.5: '이 강의의 목적 달성',
        4: '이 강의 듣길 잘함',
        4.5: '한학기 동안 많은 것을 알게됨',
        5: '특급 명강의',
    }
});

$('.view').rating('refresh', {disabled: false, showClear: false, showCaption: false});

$(window).load(function () {
    $('#text-opinion').val('');
    $('#evl-attendent').rating('clear');
    $('#evl-grade').rating('clear');
    $('#evl-amount').rating('clear');
    $('#evl-learning').rating('clear');
});


$('#submitOpinion').click(function () {
    if ($('#text-opinion').val('') == "") {
        alert("의견을 입력해주세요");
        return false;
    } else {
        return true;
    }
});


$('#closeOpinion').click(function () {
    if (confirm("종료하시면 입력하고있는 평가는 삭제됩니다.") == true) {
        $('#text-opinion').val('');
        $('#evl-attendent').rating('clear');
        $('#evl-grade').rating('clear');
        $('#evl-amount').rating('clear');
        $('#evl-learning').rating('clear');
    } else {
        return false;
    }
});

