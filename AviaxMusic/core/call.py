async def change_stream(self, client, chat_id):
    check = db.get(chat_id)
    popped = None
    loop = await get_loop(chat_id)
    try:
        if loop == 0:
            popped = check.pop(0)
        else:
            loop = loop - 1
            await set_loop(chat_id, loop)
        await auto_clean(popped)
        if not check:
            await _clear_(chat_id)
            return await client.leave_group_call(chat_id)
    except:
        try:
            await _clear_(chat_id)
            return await client.leave_group_call(chat_id)
        except:
            return
    else:
        queued = check[0]["file"]
        language = await get_lang(chat_id)
        _ = get_string(language)
        title = (check[0]["title"]).title()
        user = check[0]["by"]
        original_chat_id = check[0]["chat_id"]
        streamtype = check[0]["streamtype"]
        videoid = check[0]["vidid"]
        db[chat_id][0]["played"] = 0
        exis = (check[0]).get("old_dur")
        if exis:
            db[chat_id][0]["dur"] = exis
            db[chat_id][0]["seconds"] = check[0]["old_second"]
            db[chat_id][0]["speed_path"] = None
            db[chat_id][0]["speed"] = 1.0
        video = True if str(streamtype) == "video" else False

        # Thumbnail ko ignore kar diya, sirf default image use hoga
        default_img = config.STREAM_IMG_URL
        button = stream_markup(_, chat_id)

        if "live_" in queued or "vid_" in queued or "index_" in queued:
            stream = AudioVideoPiped(queued, audio_parameters=HighQualityAudio(),
                                     video_parameters=MediumQualityVideo()) if video else AudioPiped(queued, audio_parameters=HighQualityAudio())
            try:
                await client.change_stream(chat_id, stream)
            except:
                return await app.send_message(original_chat_id, text=_["call_6"])
            
            run = await app.send_photo(chat_id=original_chat_id, photo=default_img,
                                       caption=_["stream_1"].format(
                                           f"https://t.me/{app.username}?start=info_{videoid}",
                                           title[:23], check[0]["dur"], user),
                                       reply_markup=InlineKeyboardMarkup(button))
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
        else:
            # fallback for other queued types
            stream = AudioVideoPiped(queued, audio_parameters=HighQualityAudio(),
                                     video_parameters=MediumQualityVideo()) if video else AudioPiped(queued, audio_parameters=HighQualityAudio())
            try:
                await client.change_stream(chat_id, stream)
            except:
                return await app.send_message(original_chat_id, text=_["call_6"])
            
            run = await app.send_photo(chat_id=original_chat_id, photo=default_img,
                                       caption=_["stream_1"].format(
                                           f"https://t.me/{app.username}?start=info_{videoid}",
                                           title[:23], check[0]["dur"], user),
                                       reply_markup=InlineKeyboardMarkup(button))
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
