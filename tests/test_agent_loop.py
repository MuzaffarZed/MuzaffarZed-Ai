"""tests/test_agent_loop.py - Unit tests for ReAct AgentLoop."""

import pytest
from brain.agent_loop import AgentLoop, get_agent_loop, SubGoal, TaskResult


def test_agent_loop_singleton():
    loop1 = get_agent_loop()
    loop2 = get_agent_loop()
    assert loop1 is loop2
    assert isinstance(loop1, AgentLoop)


def test_agent_loop_offline_planner_usb():
    loop = AgentLoop()
    goals = loop.plan_offline("Fleshkadagi barcha rasmlarni yangi papkaga olib o't")
    assert len(goals) >= 2
    tool_names = [g.tool_name for g in goals]
    assert "get_drives" in tool_names or "run_powershell" in tool_names
    assert goals[-1].tool_name == "finish_task"


def test_agent_loop_offline_planner_weather():
    loop = AgentLoop()
    goals = loop.plan_offline("Brauzerni ochib ob-havoni ko'r va Bloknotga yoz")
    assert len(goals) >= 3
    tool_names = [g.tool_name for g in goals]
    assert "launch_application" in tool_names
    assert "type_text_unicode" in tool_names


def test_agent_loop_offline_planner_archive():
    loop = AgentLoop()
    goals = loop.plan_offline("Telegramdan faylni yuklab arxivdan chiqar")
    assert len(goals) >= 2
    tool_names = [g.tool_name for g in goals]
    assert "run_powershell" in tool_names


def test_agent_loop_tool_execution():
    loop = AgentLoop()
    res = loop.execute_tool("run_powershell", {"command": "Write-Output 'Test OK'"})
    assert res.get("success") is True

    res_finish = loop.execute_tool("finish_task", {"summary": "Bajarildi", "success": True})
    assert res_finish.get("success") is True
    assert res_finish.get("message") == "Bajarildi"


def test_agent_loop_run_task_cycle():
    loop = AgentLoop()
    steps_tracked = []

    def cb(s, thought, tool):
        steps_tracked.append((s, thought, tool))

    result = loop.run_task("Ob-havoni tekshir va Bloknotga yozib ber", on_step_callback=cb)
    assert isinstance(result, TaskResult)
    assert result.success is True
    assert len(result.steps) > 0
    assert len(steps_tracked) > 0


def test_agent_loop_notepad_multistep():
    loop = AgentLoop()
    command = "Notepad dasturini och, 'Muhandis Muzaffar uchun ReAct tizimi faollashtirildi' deb yoz va oynani minimallashtir"
    goals = loop.plan_offline(command)
    assert len(goals) >= 3
    tool_names = [g.tool_name for g in goals]
    assert "run_powershell" in tool_names or "launch_application" in tool_names
    assert "type_text_unicode" in tool_names
    assert "press_hotkey" in tool_names
    assert goals[-1].tool_name == "finish_task"

    # execute_goal testi
    summary = loop.execute_goal(command)
    assert isinstance(summary, str)
    assert len(summary) > 0
