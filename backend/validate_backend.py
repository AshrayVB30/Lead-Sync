"""
Backend validation script to check for common issues.
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test all imports"""
    print("🔍 Testing imports...")
    try:
        from models.schemas import Lead, NoteCreate, NoteResponse, SummaryRequest, SummaryResponse
        print("  ✅ models.schemas")
    except Exception as e:
        print(f"  ❌ models.schemas: {e}")
        return False
    
    try:
        from services.leads_service import fetch_leads
        print("  ✅ services.leads_service")
    except Exception as e:
        print(f"  ❌ services.leads_service: {e}")
        return False
    
    try:
        from services.ai_service import generate_summary
        print("  ✅ services.ai_service")
    except Exception as e:
        print(f"  ❌ services.ai_service: {e}")
        return False
    
    try:
        from storage.json_store import store
        print("  ✅ storage.json_store")
    except Exception as e:
        print(f"  ❌ storage.json_store: {e}")
        return False
    
    try:
        from routes import leads, notes
        print("  ✅ routes.leads")
        print("  ✅ routes.notes")
    except Exception as e:
        print(f"  ❌ routes: {e}")
        return False
    
    try:
        from main import app
        print("  ✅ main.app")
    except Exception as e:
        print(f"  ❌ main.app: {e}")
        return False
    
    return True

def test_pydantic_models():
    """Test Pydantic model validation"""
    print("\n🔍 Testing Pydantic models...")
    try:
        from models.schemas import Lead, NoteCreate
        
        # Test Lead model
        lead = Lead(name="Test User", email="test@example.com", phone="123-456-7890")
        print(f"  ✅ Lead model: {lead.name}")
        
        # Test NoteCreate model
        note = NoteCreate(email="test@example.com", note="Test note")
        print(f"  ✅ NoteCreate model: {note.email}")
        
        # Test invalid email
        try:
            invalid_lead = Lead(name="Test", email="invalid-email", phone="123")
            print("  ❌ Email validation not working")
            return False
        except Exception:
            print("  ✅ Email validation working")
        
        return True
    except Exception as e:
        print(f"  ❌ Pydantic validation error: {e}")
        return False

def test_json_store():
    """Test JSON storage"""
    print("\n🔍 Testing JSON storage...")
    try:
        from storage.json_store import JSONStore
        import tempfile
        import os
        
        # Create temporary store
        temp_file = os.path.join(tempfile.gettempdir(), "test_notes.json")
        test_store = JSONStore(filename=temp_file)
        
        # Test save
        test_store.save_note("test@example.com", "Test note", "Test summary")
        print("  ✅ Save note")
        
        # Test retrieve
        note = test_store.get_note("test@example.com")
        if note and note["note"] == "Test note":
            print("  ✅ Retrieve note")
        else:
            print("  ❌ Retrieve note failed")
            return False
        
        # Test get all
        all_notes = test_store.get_all_notes()
        if "test@example.com" in all_notes:
            print("  ✅ Get all notes")
        else:
            print("  ❌ Get all notes failed")
            return False
        
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        return True
    except Exception as e:
        print(f"  ❌ JSON store error: {e}")
        return False

def test_fastapi_app():
    """Test FastAPI app configuration"""
    print("\n🔍 Testing FastAPI app...")
    try:
        from main import app
        
        # Check routes
        routes = [route.path for route in app.routes]
        print(f"  ℹ️  Found {len(routes)} routes")
        
        required_routes = ["/", "/leads", "/notes", "/summary"]
        for route in required_routes:
            if any(route in r for r in routes):
                print(f"  ✅ Route {route} exists")
            else:
                print(f"  ❌ Route {route} missing")
                return False
        
        # Check middleware
        if any("CORS" in str(m) for m in app.user_middleware):
            print("  ✅ CORS middleware configured")
        else:
            print("  ⚠️  CORS middleware not found")
        
        return True
    except Exception as e:
        print(f"  ❌ FastAPI app error: {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 Backend Validation Tests")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Pydantic Models", test_pydantic_models()))
    results.append(("JSON Storage", test_json_store()))
    results.append(("FastAPI App", test_fastapi_app()))
    
    print("\n" + "=" * 60)
    print("📊 Test Results")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed! Backend is ready.")
    else:
        print("❌ Some tests failed. Please review errors above.")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
