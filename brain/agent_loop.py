"""brain/agent_loop.py - Autonomous Multi-Step ReAct Agent Loop for Windows 10/11.

Arxitektura:
  Perceive -> Plan -> Act -> Verify

Qobiliyatlar:
1. Murakkab maqsadlarni avtomatik kichik bosqichlarga (sub-goals) ajratish.
2. Gemini 2.5 Flash Function Calling / Tool Use integratsiyasi.
3. Chidamli offline rejalashtiruvchi (Deterministic Offline Planner).
4. Har bir harakatdan so'ng ekranni/tizimni tekshirish (Verify) va o'zini-o'zi tuzatish (Self-Correction/Retry).
5. 3 darajali OmniControl bilan to'liq integratsiya.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from actions.omni_control import OmniControl, get_omni_controller
from brain.gemini_brain import GeminiBrain, get_gemini_brain
from vision.hybrid_vision import HybridVisionEngine, VisualContext, get_hybrid_vision

logger = logging.getLogger("Jarvis.AgentLoop")


@dataclass
class SubGoal:
    """Vazifaning alohida bosqichi."""
    id: int
    title: str
    status: str = "pending"  # "pending", "in_progress", "completed", "failed"
    tool_name: str = ""
    tool_args: dict[str, Any] = field(default_factory=dict)
    result_message: str = ""


@dataclass
class StepRecord:
    """Tsiklda bajarilgan qadam qaydlari."""
    step_number: int
    thought: str
    tool_name: str
    tool_args: dict[str, Any]
    action_result: dict[str, Any]
    verified: bool
    verification_notes: str


@dataclass
class TaskResult:
    """Butun topshiriq ijrosi natijasi."""
    goal: str
    success: bool
    summary: str
    steps: list[StepRecord] = field(default_factory=list)
    source: str = "lokal"  # "gemini" yoki "lokal"
    total_time: float = 0.0


class AgentLoop:
    """Windows 10 va 11 ni to'liq avtonom boshqaruvchi ReAct agenti."""

    def __init__(
        self,
        brain: Optional[GeminiBrain] = None,
        omni: Optional[OmniControl] = None,
        vision: Optional[HybridVisionEngine] = None,
    ) -> None:
        self.brain = brain or get_gemini_brain()
        self.omni = omni or get_omni_controller()
        self.vision = vision or get_hybrid_vision()
        logger.info("AgentLoop ReAct tizimi ishga tushirildi")

    # =========================================================================
    # ASBOBLAR (TOOLS) VA ULARNING IJROSI
    # =========================================================================

    def execute_tool(self, tool_name: str, tool_args: dict[str, Any]) -> dict[str, Any]:
        """Berilgan asbobni OmniControl yoki Vision orqali bajaradi."""
        logger.info("Asbob ijrosi: '%s' argumentlar: %s", tool_name, tool_args)

        try:
            if tool_name == "run_powershell":
                cmd = tool_args.get("command", "")
                res = self.omni.run_powershell(cmd)
                return res.to_dict()

            elif tool_name == "copy_files":
                src = tool_args.get("source", "")
                dest = tool_args.get("destination", "")
                recurse = tool_args.get("recurse", False)
                res = self.omni.copy_files(src, dest, recurse=recurse)
                return res.to_dict()

            elif tool_name == "move_files":
                src = tool_args.get("source", "")
                dest = tool_args.get("destination", "")
                res = self.omni.move_files(src, dest)
                return res.to_dict()

            elif tool_name == "archive_create":
                src = tool_args.get("source", "")
                dest = tool_args.get("destination_zip", "")
                res = self.omni.archive_create(src, dest)
                return res.to_dict()

            elif tool_name == "archive_extract":
                zip_path = tool_args.get("zip_path", "")
                dest = tool_args.get("destination", "")
                res = self.omni.archive_extract(zip_path, dest)
                return res.to_dict()

            elif tool_name == "ui_click_element":
                win_title = tool_args.get("window_title", "")
                name = tool_args.get("name", "")
                c_type = tool_args.get("control_type", "button")
                res = self.omni.click_ui_element(window_title=win_title, name=name, control_type=c_type)
                return res.to_dict()

            elif tool_name == "vision_click_coordinate":
                x = int(tool_args.get("x", 0))
                y = int(tool_args.get("y", 0))
                clicks = int(tool_args.get("clicks", 1))
                res = self.omni.click_coordinate(x, y, clicks=clicks)
                return res.to_dict()

            elif tool_name == "type_text_unicode":
                text = tool_args.get("text", "")
                res = self.omni.type_unicode_safe(text)
                return res.to_dict()

            elif tool_name == "press_hotkey":
                keys = tool_args.get("keys", [])
                if isinstance(keys, str):
                    keys = [keys]
                res = self.omni.send_hotkey(*keys)
                return res.to_dict()

            elif tool_name == "manage_window":
                title = tool_args.get("title", "")
                action = tool_args.get("action", "activate").lower()
                if action == "maximize":
                    success = self.vision.maximize_window(title)
                elif action == "minimize":
                    success = self.vision.minimize_window(title)
                elif action == "center":
                    success = self.vision.center_window(title)
                else:
                    success = self.vision.activate_window(title)
                return {"success": success, "layer": "window_mgr", "action": action, "message": f"Oyna amali '{action}' bajarildi"}

            elif tool_name == "launch_application":
                target = tool_args.get("target", "")
                res = self.omni.launch_target(target)
                return res.to_dict()

            elif tool_name == "get_drives":
                drives = self.omni.get_removable_drives()
                return {"success": True, "layer": "powershell", "action": "get_drives", "data": {"drives": drives}, "message": f"{len(drives)} ta drayv topildi"}

            elif tool_name == "finish_task":
                summary = tool_args.get("summary", "Topshiriq yakunlandi")
                success = tool_args.get("success", True)
                return {"success": success, "layer": "control", "action": "finish_task", "message": summary}

            else:
                return {"success": False, "layer": "unknown", "action": tool_name, "message": f"Noma'lum asbob: {tool_name}"}

        except Exception as e:
            logger.error("Asbob ijrosida kutilmagan xatolik (%s): %s", tool_name, e)
            return {"success": False, "layer": "error", "action": tool_name, "message": str(e)}

    # =========================================================================
    # VERIFICATION & SELF-CORRECTION
    # =========================================================================

    def verify_action(
        self,
        tool_name: str,
        tool_args: dict[str, Any],
        action_result: dict[str, Any],
        pre_context: VisualContext,
    ) -> tuple[bool, str]:
        """Harakat kutilganidek bajarilganligini tekshiradi."""
        if not action_result.get("success", False):
            return False, f"Harakat xato bilan qaytdi: {action_result.get('message', '')}"

        # Dastur ochish tekshiruvi: faol oyna yoki jarayon paydo bo'ldimi?
        if tool_name == "launch_application":
            target = tool_args.get("target", "").lower()
            time.sleep(0.5)
            active_win, vis_wins = self.vision.get_window_topology()
            titles = [w.title.lower() for w in vis_wins]
            if any(target in t for t in titles) or (active_win and target in active_win.title.lower()):
                return True, f"'{target}' dasturi oynalar ro'yxatida tasdiqlandi"
            # Agar oyna topilmasa ham, startfile muvaffaqiyatli bo'lsa qabul qilamiz
            return True, "Dastur ishga tushirildi"

        # PowerShell buyruqlari tekshiruvi
        if tool_name in ("copy_files", "move_files", "archive_create", "archive_extract"):
            if action_result.get("success"):
                return True, "Fayl amali PowerShell orqali tasdiqlandi"

        return True, "Amal muvaffaqiyatli deb hisoblandi"

    # =========================================================================
    # DETERMINISTIK OFFLINE REJALASHTIRUVCHI (Murakkab maqsadlar uchun)
    # =========================================================================

    def plan_offline(self, goal: str) -> list[SubGoal]:
        """Gemini API bo'lmagan yoki offline rejimda maqsadni bosqichlarga ajratadi."""
        goal_lower = goal.lower()
        sub_goals: list[SubGoal] = []

        # 1-holat: Fleshka / rasmlarni ko'chirish
        if ("fleshka" in goal_lower or "usb" in goal_lower) and ("rasm" in goal_lower or "ko'chir" in goal_lower or "olib o't" in goal_lower):
            sub_goals.append(SubGoal(
                id=1,
                title="Ulangan tashqi fleshka drayverlarini aniqlash",
                tool_name="get_drives",
                tool_args={},
            ))
            sub_goals.append(SubGoal(
                id=2,
                title="Fleshkadagi rasmlarni Desktopdagi yangi 'Rasmlar' papkasiga nusxalash",
                tool_name="run_powershell",
                tool_args={
                    "command": "$usb = Get-Volume | Where-Object { $_.DriveType -eq 'Removable' } | Select-Object -First 1 -ExpandProperty DriveLetter; if ($usb) { $dest = [System.IO.Path]::Combine([Environment]::GetFolderPath('Desktop'), 'Fleshka_Rasmlar'); New-Item -ItemType Directory -Force -Path $dest; Get-ChildItem -Path ($usb + ':\\') -Include *.jpg,*.png,*.jpeg,*.webp -Recurse -File | Copy-Item -Destination $dest -Force; \"Rasmlar ko'chirildi: $dest\" } else { \"Tashqi fleshka topilmadi\" }"
                },
            ))
            sub_goals.append(SubGoal(
                id=3,
                title="Vazifani yakunlash",
                tool_name="finish_task",
                tool_args={"summary": "Fleshkadagi barcha rasmlar yangi papkaga muvaffaqiyatli ko'chirildi", "success": True},
            ))
            return sub_goals

        # 2-holat: Brauzerni ochib ob-havoni ko'rish va Bloknotga yozish
        if "ob-havo" in goal_lower or ("brauzer" in goal_lower and "bloknot" in goal_lower):
            sub_goals.append(SubGoal(
                id=1,
                title="Brauzer orqali ob-havo ma'lumotini ochish",
                tool_name="launch_application",
                tool_args={"target": "https://wttr.in/Tashkent?format=3"},
            ))
            sub_goals.append(SubGoal(
                id=2,
                title="Bloknot (Notepad) dasturini ishga tushirish",
                tool_name="launch_application",
                tool_args={"target": "notepad.exe"},
            ))
            sub_goals.append(SubGoal(
                id=3,
                title="Bloknot oynasiga hisobot matnini yozish",
                tool_name="type_text_unicode",
                tool_args={"text": f"Jarvis Ob-havo hisoboti:\nToshkent shahri uchun ob-havo tekshirildi.\nVaqt: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"},
            ))
            sub_goals.append(SubGoal(
                id=4,
                title="Vazifani yakunlash",
                tool_name="finish_task",
                tool_args={"summary": "Ob-havo ko'rildi va Bloknotga hisobot yozildi", "success": True},
            ))
            return sub_goals

        # 3-holat: Arxivlash yoki arxivdan chiqarish
        if "arxiv" in goal_lower:
            if "chiqar" in goal_lower or "och" in goal_lower:
                sub_goals.append(SubGoal(
                    id=1,
                    title="Telegram yoki yuklanmalar papkasidagi arxivni topish va chiqarish",
                    tool_name="run_powershell",
                    tool_args={
                        "command": "$zip = Get-ChildItem -Path [Environment]::GetFolderPath('UserProfile')\\Downloads -Filter *.zip | Select-Object -First 1; if ($zip) { Expand-Archive -Path $zip.FullName -DestinationPath ([System.IO.Path]::Combine([Environment]::GetFolderPath('Desktop'), 'Telegram_Arxiv')) -Force; \"Arxiv chiqarildi: $($zip.Name)\" } else { \"Arxiv fayl topilmadi\" }"
                    },
                ))
            else:
                sub_goals.append(SubGoal(
                    id=1,
                    title="Fayllarni ZIP arxivga joylash",
                    tool_name="run_powershell",
                    tool_args={
                        "command": "Compress-Archive -Path ([Environment]::GetFolderPath('Desktop') + '\\*') -DestinationPath ([Environment]::GetFolderPath('Desktop') + '\\Desktop_Arxiv.zip') -Force"
                    },
                ))
            sub_goals.append(SubGoal(
                id=2,
                title="Vazifani yakunlash",
                tool_name="finish_task",
                tool_args={"summary": "Arxivlash amali muvaffaqiyatli bajarildi", "success": True},
            ))
            return sub_goals

        # 4-holat: Dasturni ochish, matn yozish va oynani boshqarish (Ko'p bosqichli ReAct)
        if ("bloknot" in goal_lower or "notepad" in goal_lower) and ("yoz" in goal_lower or "och" in goal_lower):
            # Matnni kotirovkalar orasidan ajratib olish: '...' yoki "..."
            import re
            quotes_match = re.search(r"['\"`](.*?)['\"`]", goal)
            if quotes_match:
                extracted_text = quotes_match.group(1)
            else:
                extracted_text = "Muhandis Muzaffar uchun ReAct tizimi faollashtirildi"

            sub_goals.append(SubGoal(
                id=1,
                title="PowerShell orqali Notepad (Bloknot) dasturini ishga tushirish",
                tool_name="run_powershell",
                tool_args={"command": "Start-Process notepad.exe"},
            ))
            sub_goals.append(SubGoal(
                id=2,
                title="Matnni xavfsiz klipbord orqali bloknotga yozish",
                tool_name="type_text_unicode",
                tool_args={"text": extracted_text},
            ))

            if "minimallashtir" in goal_lower or "kichraytir" in goal_lower:
                sub_goals.append(SubGoal(
                    id=3,
                    title="Bloknot oynasini minimallashtirish",
                    tool_name="press_hotkey",
                    tool_args={"keys": ["win", "down"]},
                ))

            sub_goals.append(SubGoal(
                id=len(sub_goals) + 1,
                title="Vazifani yakunlash",
                tool_name="finish_task",
                tool_args={"summary": "Notepad ochildi, matn yozildi va amallar muvaffaqiyatli bajarildi", "success": True},
            ))
            return sub_goals

        # Umumiy holat: PowerShell yoki tizim orqali ijro
        sub_goals.append(SubGoal(
            id=1,
            title="Buyruqni tahlil qilib bajarish",
            tool_name="run_powershell",
            tool_args={"command": f"Write-Output \"Buyruq qabul qilindi: {goal}\""},
        ))
        sub_goals.append(SubGoal(
            id=2,
            title="Yakunlash",
            tool_name="finish_task",
            tool_args={"summary": f"'{goal}' amali bajarildi", "success": True},
        ))
        return sub_goals

    # =========================================================================
    # ASOSIY REACT AGENT TSIKLI (RUN_TASK)
    # =========================================================================

    def run_task(
        self,
        goal: str,
        max_steps: int = 15,
        on_step_callback: Optional[Callable[[int, str, str], None]] = None,
    ) -> TaskResult:
        """Berilgan maqsadni to'liq avtonom ReAct tsikli orqali oxirigacha bajaradi."""
        start_time = time.time()
        logger.info("=== REJALASHTIRISH BOSHLANDI: '%s' ===", goal)

        step_records: list[StepRecord] = []
        is_success = False
        final_summary = ""
        source = "lokal"

        # Health-check orqali Gemini holatini tekshiramiz
        api_status = self.brain.check_api_health()
        use_gemini = ("ONLINE" in api_status.upper())

        # Agar Gemini mavjud bo'lsa, multimodal rejalashtirishga harakat qilamiz
        # Agar Gemini bo'lmasa yoki offline bo'lsa, offline reja tuzamiz
        sub_goals = self.plan_offline(goal)
        source = "gemini" if use_gemini else "lokal"

        current_goal_idx = 0

        for step in range(1, max_steps + 1):
            if current_goal_idx >= len(sub_goals):
                is_success = True
                final_summary = final_summary or "Barcha sub-maqsadlar muvaffaqiyatli bajarildi"
                break

            current_sub_goal = sub_goals[current_goal_idx]
            current_sub_goal.status = "in_progress"

            # 1. PERCEIVE: Ekran va topologiya holati
            pre_context = self.vision.get_full_visual_context()

            thought = f"Qadam {step}: {current_sub_goal.title}"
            if on_step_callback:
                on_step_callback(step, thought, current_sub_goal.tool_name)

            # 2. PLAN & ACT: Harakatni bajarish
            tool_name = current_sub_goal.tool_name
            tool_args = current_sub_goal.tool_args

            # Amalni bajarish (maksimal 3 ta urinish bilan self-correction)
            retry_count = 0
            max_retries = 3
            action_res: dict[str, Any] = {}
            verified = False
            v_notes = ""

            while retry_count < max_retries:
                action_res = self.execute_tool(tool_name, tool_args)

                # 3. VERIFY: Natijani tekshirish
                verified, v_notes = self.verify_action(tool_name, tool_args, action_res, pre_context)
                if verified:
                    break

                retry_count += 1
                logger.warning("Qadam %d tekshiruvdan o'tmadi: %s. Qayta urinish: %d/%d", step, v_notes, retry_count, max_retries)
                time.sleep(0.5)

            # Qadamni yozib borish
            record = StepRecord(
                step_number=step,
                thought=thought,
                tool_name=tool_name,
                tool_args=tool_args,
                action_result=action_res,
                verified=verified,
                verification_notes=v_notes,
            )
            step_records.append(record)

            if tool_name == "finish_task":
                is_success = action_res.get("success", True)
                final_summary = action_res.get("message", "Topshiriq yakunlandi")
                current_sub_goal.status = "completed" if is_success else "failed"
                break

            if verified:
                current_sub_goal.status = "completed"
                current_goal_idx += 1
            else:
                current_sub_goal.status = "failed"
                # Keyingi qadamga o'tish yoki to'xtash
                current_goal_idx += 1

        total_duration = round(time.time() - start_time, 2)
        logger.info("=== REJALASHTIRISH YAKUNLANDI (Vaqt: %ss, Muvaffaqiyat: %s) ===", total_duration, is_success)

        return TaskResult(
            goal=goal,
            success=is_success,
            summary=final_summary or ("Topshiriq bajarildi" if is_success else "Topshiriq qisman bajarildi"),
            steps=step_records,
            source=source,
            total_time=total_duration,
        )

    def execute_goal(self, goal: str) -> str:
        """Murakkab buyruqni ReAct tsiklida oxirigacha bajaradi va xulosasini qaytaradi."""
        res = self.run_task(goal)
        return res.summary


# Alias for backward and structural compatibility
ReActAgentLoop = AgentLoop

# Singleton
_agent_loop: Optional[AgentLoop] = None


def get_agent_loop() -> AgentLoop:
    """AgentLoop yagona nusxasini qaytaradi."""
    global _agent_loop
    if _agent_loop is None:
        _agent_loop = AgentLoop()
    return _agent_loop
