def template(input:str = "") -> tuple[str,str]:
    prompt:str = f"{input}, "
    negative_prompt:str = " "
    return prompt, negative_prompt

def portrait_animated_disney(input:str = "elsa") -> tuple[str,str]:
    
    prompt:str = f"{input}, d & d, fantasy, intricate, elegant, highly detailed, digital painting, artstation, concept art, matte, sharp focus, illustration, art by artgerm, greg rutkowski, alphonse mucha, 8k"
    
    negative_prompt:str = "deformed, cripple, ugly, additional arms, additional legs, additional head, two heads, multiple people, group of people"
    
    return prompt, negative_prompt

def portrait_art_lineart(input:str = "strong warrior princess") -> tuple[str,str]:
    
    prompt:str = f"{input}, portrait | centered| key visual| intricate| highly detailed| breathtaking beauty| precise lineart| vibrant| comprehensive cinematic| Carne Griffiths| Conrad Roset"
    
    negative_prompt:str = " "
    
    return prompt, negative_prompt

def portrait_photorealistic_female_snow(input: str = "gorgeous Norwegian girl in winter clothing with long wavy blonde hair") -> tuple[str, str]:
    
    prompt: str = f"professional portrait photograph of a {input}, ((sultry flirty look)), freckles, beautiful symmetrical face, cute natural makeup, ((standing outside in snowy city street)), stunning modern urban upscale environment, ultra realistic, concept art, elegant, highly detailed, intricate, sharp focus, depth of field, f/1. 8, 85mm, medium shot, mid shot, (centered image composition), (professionally color graded), ((bright soft diffused light)), volumetric fog, trending on instagram, trending on tumblr, hdr 4k, 8k"
    
    negative_prompt: str = "(bonnet), (hat), (beanie), cap, (((wide shot))), (cropped head), bad framing, out of frame, deformed, cripple, old, fat, ugly, poor, missing arm, additional arms, additional legs, additional head, additional face, multiple people, group of people, dyed hair, black and white, grayscale"
    
    return prompt, negative_prompt

def portrait_photorealistic_korean_woman(input:str = "") -> tuple[str,str]:
    
    prompt:str = f"{input}, (masterpiece:1. 0), (best quality:1. 4), (ultra highres:1. 2), (photorealistic:1. 4), (8k, RAW photo:1. 2), (soft focus:1. 4), 1 woman, posh, (sharp focus:1. 4), (korean:1. 2), (american:1. 1), detailed beautiful face, black hair, (detailed open blazer:1. 4), tie, beautiful white shiny humid skin, smiling"
    
    negative_prompt:str = "illustration, 3d, sepia, painting, cartoons, sketch, (worst quality:2), (low quality:2), (normal quality:2), lowres, bad anatomy, bad hands, normal quality, ((monochrome)), ((grayscale:1.2)),newhalf, collapsed eyeshadow, multiple eyebrows, pink hair, analog, analogphoto"
    
    return prompt, negative_prompt

def portrait_photorealistic_white_woman(input:str = "a few freckles, round eyes and short messy hair") -> tuple[str,str]:
    
    prompt:str = f"detailed and realistic portrait of a woman with {input} outside, wearing a white t shirt, staring at camera, chapped lips, soft natural lighting, portrait photography, magical photography, dramatic lighting, photo realism, ultra-detailed, intimate portrait composition, Leica 50mm, f1. 4"
    
    negative_prompt:str = " "
    
    return prompt, negative_prompt

def portrait_art_19thcenturypainting(input:str = "old coal miner") -> tuple[str,str]:
    
    prompt:str = f", a portrait of an {input} in 19th century, beautiful painting with highly detailed face by greg rutkowski and magali villanueve"
    
    negative_prompt:str = " "
    
    return prompt, negative_prompt

def portrait_art_bwpainting(input:str = "pierce brisnan as old sailor") -> tuple[str,str]:
    
    prompt:str = f"highly detailed portrait of {input}, by Dustin Nguyen, Akihiko Yoshida, Greg Tocchini, Greg Rutkowski, Cliff Chiang, 4k resolution, Dishonored inspired, bravely default inspired, vibrant but dreary red, black and white color scheme! ! ! , epic extreme long shot, dark mood and strong backlighting, volumetric lights, smoke volutes, artstation HQ, unreal engine, octane renderer, HQ, 8K"
    
    negative_prompt:str = " "
    
    return prompt, negative_prompt

def portrait_art_solarpunk(input:str = "asian girl") -> tuple[str,str]:
    
    prompt:str = f"Beautiful anime portrait painting of {input}, solarpunk summer chill day, by tim okamura, victor nizovtsev, greg rutkowski, noah bradley. trending on artstation, 8k, masterpiece, graffiti paint, fine detail, full of color, intricate detail, golden ratio illustration"
    
    negative_prompt:str = " "
    
    return prompt, negative_prompt

def landscape_animated_cyberpunk(input:str = "streets") -> tuple[str,str]:
    
    prompt:str = f"portrait art of blade runner {input} 8 k ultra realistic, lens flare, atmosphere, glow, detailed, intricate, full of colour, cinematic lighting, trending on artstation, 4 k, hyperrealistic, focused, extreme details, unreal engine 5, cinematic, masterpiece"
    
    negative_prompt:str = " "
    
    return prompt, negative_prompt

def portrait_art_anime(input:str = "warrior goddess standing alone on hill") -> tuple[str,str]:
    prompt:str = f"poster of {input} | centered| detailed gorgeous face| anime style| key visual| intricate detail| highly detailed| breathtaking| vibrant| panoramic| cinematic| Carne Griffiths| Conrad Roset| Makoto Shinkai"
    
    negative_prompt:str = "no words| watermark| bad anatomy| blurry| fuzzy| extra legs| extra arms| extra fingers| poorly drawn hands| poorly drawn feet| disfigured| out of frame| tiling| bad art| deformed| mutated| double face"
    
    return prompt, negative_prompt

def portrait_art_personification(persona:str = "the Halloween holiday", character:str ="a cute girl with short hair and a villain's smile") -> tuple[str,str]:
    
    prompt:str = f"The personification of {input} in the form of {input}, (((cute girl)))cute hats, cute cheeks, unreal engine, highly detailed, artgerm digital illustration, woo tooth, studio ghibli, deviantart, sharp focus, artstation, by Alexei Vinogradov bakery, sweets, emerald eyes"
    
    negative_prompt:str = "bad anatomy, extra legs, extra arms, poorly drawn face, poorly drawn hands, poorly drawn feet, fat, disfigured, out of frame, long neck, poo art, bad hands, bad art, deformed, gun, double head, flowers, asian, hyperrealistic, child"
    
    return prompt, negative_prompt

def portrait_photorealistic_fullbody(input:str = "paladin wearing full body (light silver armour:1. 2)") -> tuple[str,str]:
    
    prompt:str = f"full body, walking pose, slow motion, {input}, (insanely detailed, bloom:1. 5), (highest quality, Alessandro Casagrande, Greg Rutkowski, Sally Mann, concept art, 4k), (analog:1. 2), (high sharpness), (detailed pupils:1. 1), (painting:1. 1), (digital painting:1. 1), detailed face and eyes, Masterpiece, best quality, (highly detailed photo:1. 1), 8k, photorealistic, (long blonde Hair, ponytail haircut, ecstatic:1. 1), (young woman:1. 1), By jeremy mann, by sandra chevrier, by maciej kuciara, sharp, (perfect body:1. 1), realistic, real shadow, 3d, (temple background:1. 2), (by Michelangelo)"
    
    negative_prompt:str = "jpeg artifacts, low quality, lowres, 3d, render, doll, plastic, blur, haze, monochrome, b&w, text, (ugly:1.2), unclear eyes, no arms, bad anatomy, cropped, censoring, asymmetric eyes, bad anatomy, bad proportions, cropped, cross-eyed, deformed, extra arms, extra fingers, extra limbs, fused fingers, malformed, mangled hands, misshapen body, missing arms, missing fingers, missing hands, missing legs, poorly drawn, tentacle finger, too many arms, too many fingers, watermark, logo, text, letters, signature, username, words, blurry, cropped"
    
    return prompt, negative_prompt

def portrait_animated_tarot(input:str = "cyberpunk head") -> tuple[str,str]:
    prompt:str = f"((tarot card with intricate detailed frame around the outside)) | side profile of {input} with large moon in background| cyberpunk | styled in Art Nouveau | insanely detailed | embellishments | high definition | concept art | digital art | vibrant"
    negative_prompt:str = "lowres| text| error| missing fingers| extra digit| fewer digits| cropped| (worst quality| low quality:1.4)| jpeg artifacts| signature| bad anatomy| extra legs| extra arms| extra fingers| poorly drawn hands| poorly drawn feet| disfigured| out of frame| tiling| bad art| deformed| mutated| blurry| fuzzy| misshaped| mutant| gross| disgusting| ugly| watermark| watermarks"
    return prompt, negative_prompt

def anime_spacegirl(input:str = "") -> tuple[str,str]:
    
    prompt:str = f"{input}, space girl| standing alone on hill| centered| detailed gorgeous face| anime style| key visual| intricate detail| highly detailed| breathtaking| vibrant| panoramic| cinematic| Carne Griffiths| Conrad Roset| ghibli"
    
    negative_prompt:str = "deformed, cripple, ugly, additional arms, additional legs, additional head, two heads, multiple people, group of people"
    
    return prompt, negative_prompt

def anime_model_racecar(input:str = "") -> tuple[str,str]:
    
    prompt:str = f"{input}, modelshoot style, (film stock), (film grain), (extremely detailed CG unity 8k wallpaper), full body portrait of the most beautiful woman in the world, (cowboy shot), beautiful racecar woman standing in front of a race car, standing, tanned skin, (blush) (bangs), long hair, (freckles:0. 75), detailed symmetrical face, smirk, ((pink hair:1. 4)), (straight hair), (green eyes:1. 3), reflective eyes, dark eyebrows, mascara, makeup, (dark lipstick), (white sclera), dust particles, detailed lighting, rim lighting, dramatic lighting, chiaroscuro, (black crop top), ((white racing jacket)), open jacket, (white yoga pants), race track, red racecar, spoilers, road, bleachers, blue sky, white clouds, (from behind), (ass), (professional majestic impressionism oil painting by Waterhouse), John Constable, Ed Blinkey, Atey Ghailan, (Studio Ghibli), by Jeremy Mann, Greg Manchess, Antonio Moro, trending on ArtStation, trending on CGSociety, Intricate, High Detail, dramatic, makoto shinkai kyoto, trending on artstation, trending on CGsociety"
    
    negative_prompt:str = "(pink eyes), (green jacket), (poofy jacket,), ((multi colored hair)), (sweater), Iron mouse hair, blue hair, ((pink clouds)), (headband), headphones, canvas frame, cartoon, 3d, ((disfigured)), ((bad art)), ((deformed)),((extra limbs)),((close up)),((b&w)), weird colors, blurry, (((duplicate))), ((morbid)), ((mutilated)), [out of frame], extra fingers, mutated hands, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), (((deformed))), ((ugly)), blurry, ((bad anatomy)), (((bad proportions))), ((extra limbs)), cloned face, (((disfigured))), out of frame, ugly, extra limbs, (bad anatomy), gross proportions, (malformed limbs), ((missing arms)), ((missing legs)), (((extra arms))), (((extra legs))), mutated hands, (fused fingers), (too many fingers), (((long neck))), Photoshop, ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, mutation, mutated, extra limbs, extra legs, extra arms, disfigured, deformed, cross-eye, body out of frame, blurry, bad art, bad anatomy, 3d render"
    
    return prompt, negative_prompt

def chinese_woman(input:str = "") -> tuple[str,str]:

    prompt:str = f"{input}, (full_body:1. 2), best quality, (8k, RAW photo, best quality, masterpiece:1. 2), (realistic, photo-realistic:1. 4), ultra-detailed, perfect detail, looking at the viewer, pretty Filipina-Chinese mixed race lady wearing a black bathing suit, wet skin, light reflections, cute face, full body shot, long black hair, brown eyes, lite makeup, full lips"
    
    negative_prompt:str = "paintings,sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, bad anatomy,(long hair:1.4),DeepNegative,(fat:1.2),facing away, looking away,tilted head, {Multiple people}, lowres,bad anatomy,bad hands, text, error, missing fingers,extra digit, fewer digits, cropped, worstquality, low quality, normal quality,jpegartifacts,signature, watermark, username,blurry,bad feet,cropped,poorly drawn hands,poorly drawn face,mutation,deformed,worst quality,low quality,normal quality,jpeg artifacts,signature,watermark,extra fingers,fewer digits,extra limbs,extra arms,extra legs,malformed limbs,fused fingers,too many fingers,long neck,cross-eyed,mutated hands,polar lowres,bad body,bad proportions,gross proportions,text,error,missing fingers,missing arms,missing legs,extra digit, extra arms, extra leg, extra foot,nsfw"
    
    return prompt, negative_prompt

def waifu(input:str = "") -> tuple[str,str]:

    prompt:str = f"{input}, (masterpiece, best quality:1. 4), solo, pov, stunning girlfriend, (standing:1. 1), (abs:1), dynamic pose, (tight yoga pants, white yoga pants:1. 4), long blonde hair, smokey eyes makeup, depth of field, atmospheric perspective, volumetric lighting, sharp focus, absurdres, realistic proportions, good anatomy, (realistic, hyperrealistic:1. 4), 16k hdr"
    
    negative_prompt:str = "(worst quality, low quality, normal quality:1.4), lowres, bad anatomy, ((bad hands)), text, error, missing fingers, extra digit, fewer digits,head out of frame, cropped, letterboxed, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, censored, letterbox, blurry, monochrome, fused clothes, nail polish, boring, extra legs, fused legs, missing legs, missing arms, extra arms, fused arms, missing limbs, mutated limbs, dead eyes, empty eyes, 2girls, multiple girls, 1boy, 2boys, multiple boys, multiple views, jpeg artifacts, text, signature, watermark, artist name, logo, low res background, low quality background, missing background, white background"
    
    return prompt, negative_prompt
