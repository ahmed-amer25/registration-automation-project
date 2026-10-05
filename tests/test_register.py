from pages.register_page import RegisterPage

def test_clinic_registration_flow(driver):
    register_page = RegisterPage(driver)
    
    print("\n[1] فتح الصفحة واختيار العيادة...")
    register_page.open_page("https://commacare-medical.quarizm.online/auth/login")
    register_page.click_create_account()
    register_page.select_clinic_and_proceed()
    
    print("[2] تعبئة البيانات...")
    data = register_page.fill_registration_form()
    register_page.click_verify_and_submit()
    
    print("[3] إدخال OTP...")
    register_page.enter_otp_and_submit("1234")
    
    print("[4] إغلاق مودال النجاح (Complete your information)...")
    register_page.click_complete_your_information()
    
    print("[5] رسم التوقيع...")
    register_page.draw_signature()
    
    print("[6] حفظ التوقيع (Save)...")
    register_page.click_save_signature()
    
    print("[7] المتابعة للاتفاقية (Continue to Agreement)...")
    register_page.click_proceed_to_agreement()
    
    print("[8] التوقيع والموافقة على الاتفاقية...")
    register_page.click_sign_agreement()
    
    print("[9] المتابعة للعقد...")
    register_page.click_proceed_to_contract()
    
    print("[10] الانتقال للوحة التحكم...")
    register_page.click_go_to_dashboard()
    
    print("[11] التعامل مع مودال المصادقة وتسجيل الخروج...")
    register_page.click_logout_from_modal()
    
    print("✅ اكتمل الاختبار وسلسلة التسجيل بنجاح!")